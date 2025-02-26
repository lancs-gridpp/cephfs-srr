#!/usr/bin/python3
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
#    * Gerard Hand <g.hand@lancaster.ac.uk>
# 

import logging.handlers
import datetime
#from config import SystemConfig
#from storage import StorageService
from cephfs_srr.config import SystemConfig
from cephfs_srr.storage import StorageService

APP_VERSION     = "1.1.0"

def write_output_file(file_name, text):
    file = open(file_name, "w")
    file.write(text)
    file.close()


def main():
    try:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        log = logging.getLogger('cephssr')
        log.setLevel(logging.INFO)
        log.addHandler(handler)
        log.info("Storage Summary "+APP_VERSION+" started")

        config = SystemConfig()
        config.read()
        log.setLevel(config.logging_level)

        storage = StorageService(config.hostname, config.implementation, config.implementationversion, config.quality_level)
        storage.add_endpoints(config.endpoints())
        storage.add_shares(config.shares())
        json = storage.to_json()

        if config.output_to_file():
            write_output_file(config.output_file, json)
            log.info("SRR json file created '%s'",config.output_file)
        else:
            print(json)
            log.info("SRR json output to console")

    except Exception as e:
        log.error("unable to create SRR json for CephFS: %s", str(e))


if __name__ == "__main__":
    main()
