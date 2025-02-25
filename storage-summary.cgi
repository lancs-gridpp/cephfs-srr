#!/usr/bin/python3
# CGI storage-summary.py
#
#
# Copyright (c) 2022, University of Lancaster
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the University of Lancaster nor the names of
#     its contributors may be used to endorse or promote products
#     derived from this software without specific prior written
#     permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Contributors:
#
#   * Gerard Hand <g.hand@lancaster.ac.uk>
#
#
import logging.handlers
import datetime
from config import SystemConfig
from storage import StorageService

APP_VERSION = "1.1.0"

try:
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    log = logging.getLogger('cephssr')
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    log.info("Storage-Summary "+APP_VERSION+" started")

    config = SystemConfig()
    config.read()
    log.setLevel(config.logging_level)

    storage = StorageService(config.hostname, config.implementation, config.quality_level)
    storage.add_endpoints(config.endpoints())
    storage.add_shares(config.shares())
    json = storage.to_json()

    sys.stdout.write("Content-type: application/json\r\n\r\n")
    sys.stdout.write(json);

except Exception as e:
    sys.stdout.write("Status: 503 SRR Unavailable\r\n")
    sys.stdout.write("Retry-After: 600\r\n")
    sys.stdout.write("Content-Type: text/html\r\n\r\n")
    sys.stdout.write("<h1>Unable to access the storage details</h1>\r\n")
