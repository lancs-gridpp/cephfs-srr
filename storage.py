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
#

import json
import logging
import subprocess
import time

log = logging.getLogger('cephssr')

# Holds the storage information and creates a JSON string.
class StorageService(object):

    def __init__(self, host):
        self.timestamp = int(time.time())
        self.data = {}
        self.data["datastores"] = []
        self.data["latestupdate"] = self.timestamp
        self.data["name"] = host
        self.data["implementation"] = "CEPHFS"
        self.data["implementationversion"] = "0.1"
        self.data["qualitylevel"] = "production"
        self.data["storageshares"] = []
        self.data["storageendpoints"] = []

    # Get the number of bytes in a directory (and subdirectories) from the 'ceph.dir.rbytes' attribute.
    # Returns 0 if there is a problem getting the value.
    def get_space_used(self, path):
        try:
            ret = int(
                subprocess.check_output(
                    "getfattr -n ceph.dir.rbytes " + path + " --absolute-names --only-values; exit 0",
                    stderr=subprocess.STDOUT, shell=True).decode('utf-8'))
        except Exception as e:
            log.error("Error getting space used for path %s - Error:%s", path, str(e))
            ret = 0;
        return ret

    # Get the quota set on a directory.  This is stored in the 'ceph.quota.max_bytes' attribute.
    # Returns 0 if there is a problem getting the value.
    def get_space_available(self, path):
        try:
            ret = int(
                subprocess.check_output(
                    "getfattr -n ceph.quota.max_bytes " + path + " --absolute-names --only-values; exit 0",
                    stderr=subprocess.STDOUT, shell=True).decode('utf-8'))
        except Exception as e:
            log.error("Error getting space available for path %s - Error:%s", path, str(e))
            ret = 0;
        return ret

    # Return the total available space and the used space for a directory
    def get_storage_details(self, path):
        total = self.get_space_available(path)
        used = self.get_space_used(path)
        return total, used


    def add_shares(self, list):
        self.data["storageshares"] = []
        for item in list:
            total_size, used_size = self.get_storage_details(item["dirpath"])
            if item['totalsize'] >= 0:
                total_size = item['totalsize']
            self.data["storageshares"].append(
                StorageShare(item["name"], total_size, used_size, item["paths"], item["vos"], self.timestamp))


    def add_endpoints(self, list):
        self.data["storageendpoints"] = []
        for item in list:
            self.data["storageendpoints"].append(
                StorageEndpoint(item["name"], item["endpointurl"], item["interfacetype"]))

    # Create a JSON string for the data stored in the object.
    def to_json(self):
        ret = ''
        ret = json.dumps({"storageservice": self.data}, indent=4)
        return ret


class StorageEndpoint(dict):

    def __init__(self, name, endpointurl, interfacetype):
        self["name"] = name
        self["endpointurl"] = endpointurl
        self["interfacetype"] = interfacetype
        self["qualitylevel"] = "production"
        self["assignedshares"] = ["all"]


class StorageShare(dict):

    def __init__(self, name, total_size, used_size, paths, vos, timestamp):
        self["name"] = name
        self["timestamp"] = timestamp
        self["totalsize"] = total_size
        self["usedsize"] = used_size
        self["path"] = paths
        self["vos"] = vos
        self["assignedendpoints"] = ["all"]
        self["servingstate"] = "open"


class dataStore(dict):

    def __init__(self, name):
        self["name"] = name
        self["message"] = "Not used"
