#
#  Copyright (c) 2022, University of Lancaster
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
# 
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#    * Neither the name of the University of Lancaster nor the names of
#      its contributors may be used to endorse or promote products
#      derived from this software without specific prior written
#      permission.
# 
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
#  Contributors:
# 
#    * Gerard Hand <ghand@lancs.ac.uk>
# 

import ast
import configparser
import logging
import os
import socket

CONFIG_FILE = "/etc/cephsrr.conf"
NO_OUTPUT_FILE = ""
LOG_LEVEL = logging.INFO

log = logging.getLogger('cephssr')


# Read settings held in CONFIG_FILE
class SystemConfig(object):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.hostname = ""
        self.output_file = ""
        self.logging_level = LOG_LEVEL

    # Read the config file and process the default section.
    def read(self):
        log.debug("Reading config from "+CONFIG_FILE)
        # Read the config file.
        self.config.read(CONFIG_FILE)

        # Proess the "default" section.
        # Host name: Use fqdn if the entry isn't present in the config file or it is blank.
        self.hostname = self.config["default"].get("hostname", "")
        if self.hostname == "":
            self.hostname = socket.getfqdn()

        self.output_file = self.config["default"].get("srroutput", NO_OUTPUT_FILE)

        # Read the logging level.  If it isn't valid then don't change the default already set.
        log_levels = {'NOTSET': logging.NOTSET, 'DEBUG': logging.DEBUG, 'INFO': logging.INFO,
                      'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                      'CRITICAL': logging.CRITICAL}
        level = self.config["default"].get("logginglevel", 'INFO').strip().upper()
        if level in log_levels:
            self.logging_level = log_levels[level]
        else:
            log.error("Invalid logginglevel value: '%s'.", level)
            self.logging_level = LOG_LEVEL

    # Get a list value from the config data
    def list_value(self, section, key):
        try:
            ret = ast.literal_eval(self.config[section].get(key, "[]"))
        except Exception as e:
            log.error("Invalid list element in the config file. Section:%s,Key:%s", section, key)
            ret = []
        return ret

    # Check if all the values in a config section are set.
    def valid_section(self, section_name, settings):
        valid = True
        for key, value in settings.items():
            # Make sure that all the values are set.
            if value == "":
                valid = False
                log.error("Config file error. %s cannot be blank in section %s", key, section_name)
            if key == "exclude":
                # Make sure the "exclude" values are in the in "dir" path
                valid = valid and (len(value) == 0 or self.valid_exclude(settings["dirpath"], value))
        return valid

    # Get the "endpoint" sections from the config file.  Any endpoint sections with errors are not returned.
    def endpoints(self):
        epoints = []
        for section in self.config.sections():
            if section.startswith("endpoint"):
                epoint = {}
                epoint["name"] = self.config[section].get("name", "")
                epoint["endpointurl"] = self.config[section].get("endpointurl", "")
                epoint["interfacetype"] = self.config[section].get("interfacetype", "")
                if self.valid_section(section, epoint):
                    log.debug("Endpoint section read and is valid: %s", section)
                    epoints.append(epoint)
                else:
                    log.debug("Endpoint %s is not valid", section)
        return epoints

    # Get the "share" sections from the config file. Any share sections with errors are not returned.
    def shares(self):
        shares = []
        for section in self.config.sections():
            if section.startswith("share"):
                share = {}
                share["name"] = self.config[section].get("name", "")
                share["paths"] = self.list_value(section, "paths")
                share["vos"] = self.list_value(section, "vos")
                share["dirpath"] = self.config[section].get("dirpath", "")
                share["totalsize"] = self.convert_to_bytes(self.config[section].get("totalsize", ""))
                share["exclude"] = self.list_value(section, "exclude")
                if self.valid_section(section, share):
                    log.debug("Share section read and is valid: %s", section)
                    shares.append(share)
                else:
                    log.debug("Share %s is not valid", section)
        return shares

    # Return True iff the json should be output to a file
    def output_to_file(self):
        return self.output_file != NO_OUTPUT_FILE

    # Convert string byte value to a numeric value.  The string value can contain numbers with a suffix eg. 10MB
    def convert_to_bytes(self, str_value):
        try:
            units = {"": 1, "B": 1, "KB": 10 ** 3, "KIB": 2 ** 10, "MB": 10 ** 6, "MIB": 2 ** 20, "GB": 10 ** 9,
                     "GIB": 2 ** 30, "TB": 10 ** 12, "TIB": 2 ** 40, "PB": 10 ** 15, "PIB": 2 ** 50, "EB": 10 ** 18,
                     "EIB": 2 ** 60}
            num_ndx = 0
            while num_ndx < len(str_value):
                if str.isdigit(str_value[num_ndx]) or str_value[num_ndx] == ".":
                    num_ndx += 1
                else:
                    break
            number = float(str_value[:num_ndx])
            unit = str_value[num_ndx:].strip().upper()

            retval = int(float(number) * units[unit])
        except Exception as e:
            retval = -1
        return retval

    def valid_exclude(self, dir_path, exclude):
        valid = True
        # Make sure there is a trailing slash.
        dir_path = os.path.join(dir_path, "")
        log.debug("Checking %s is a valid exclude for %s.", exclude, dir_path)
        for item in exclude:
            if item.find(dir_path) != 0:
                log.error("%s is not a valid exlude for %s", item, dir_path)
                valid = False
                break
        if valid:
            log.debug("The exclude is valid")
        else:
            log.debug("The exlude is invalid")
        return valid
