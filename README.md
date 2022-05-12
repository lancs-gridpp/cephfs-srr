# cephfs-srr

These scripts return a SRR JSON file containing information about the endpoints and storage mounted using CephFS.  It uses *ceph.quota.max_bytes* and *ceph.dir.rbytes* to get available and used space details.

The latest version of the Storage Resource Reporting proposal can be found here:  
https://docs.google.com/document/d/1yzCvKpxsbcQC5K9MyvXc-vBF1HGPBk4vhjw3MEXoXf8/edit 


## Installation

 * Create /usr/share/cephsrr
 * Copy the python files (*.py) to /usr/share/cephsrr
 * Make sure storage-summary.py has execute permissions set.
 * Create a link (storage-summary) in /usr/bin to /usr/share/cephsrr/storage-summary.py
 * Copy cephsrr.conf to /etc and edit.

## Configuration File (cephsrr.conf)
There are 3 section types in the configuration file: default, endpoint and share.  

### Default Section
There should only be one default section defined.

```
[default]
    hostname = fal-pygrid-30.lancs.ac.uk
    srroutput = /storage/srr.json
    logginglevel = info
```
**hostname** is optional. The machines hostname is used if not specified here.
**srroutput** specifies where the output JSON should be written to.  If this is excluded the output will go to stdout.
**logginglevel** specifies the level of logging output. The options are: debug, info, warning, error, critical.

### Endpoint Sections

There can be more than one endpoint section.  Each section must have a unique name and start with *\[endpoint*. The text after *\[endpoint* and beofre *\]* is ignored.

```
[endpoing-gsiftp]
[endpoing-https]
[endpoing-xrootd]
```

```
[endpoint-https]
    name = https
    interfacetype = https
    endpointurl = https://fal-pygrid-30.lancs.ac.uk/
```

**name**, **interfacetype** and **endpointurl** values are written 'as is' to the JSON ouput.

### Share Section
There can be more than one share section.  Each section must have a unique name and start with *\[share*. The text after *\[share* and beofre *\]* is ignored.

```
[share-SKAPOOl]
[share-WLCG]
```

```
[share-WLCG]
    name = WLCG
    paths = ["/wlcg"]
    vos = ["wlcg"]
    dirpath= = /storage/wlcg
    exclude = [ "/storage/wlcg/dir1", "/storage/wlcg/dir2" ]
    totalsize = 1.1PiB
```

**name**,**paths**,**vos**,**dirpath** are written 'as is' to the the output JSON. 
**totalsize** is optional.  If this is excluded the *totalsize* for a share will be detirmined by reading the extended attribute *ceph.quota.max_butes* set on specified **dirpath**. 
Any paths specified in the **exclude** option will be excluded when calculating disc usage.



## Example SRR

https://twiki.cern.ch/twiki/pub/LCG/StorageSpaceAccounting/xrootd.srr.slac.json

```
{
    "storageservice": {
        "datastores": [], 
        "latestupdate": TIMESTAMP,
        "name": "slac.stanford.edu", 
        "implementation": "xrootd", 
        "implementationversion": "4.8.5"
        "storagecapacity" : {
            "offline" : {
                "totalsize" : 0,
                "usedsize" : 0
            },
            "online" : {
                "totalsize" : TOTALSIZE,
                "usedsize" : USEDSIZE
            }
        },
        "storageendpoints": [
            {
                "qualitylevel": "production", 
                "interfacetype": "gsiftp", 
                "name": "gsiftp", 
                "assignedshares": [
                    "all"
                ], 
                "endpointurl": "gsiftp://osggridftp02.slac.stanford.edu/"
            }, 
            {
                "qualitylevel": "testing", 
                "interfacetype": "xrootd", 
                "name": "xrootd", 
                "assignedshares": [
                    "all"
                ], 
                "endpointurl": "root://griddev03.slac.stanford.edu:2094/"
            }
        ], 
        "qualitylevel": "production", 
        "storageshares": [
            {
                "name": "ATLASDATADISK", 
                "servingstate": "open", 
                "totalsize": ATLASDATADISK_TOTALSIZE,
                "timestamp": TIMESTAMP,
                "assignedendpoints": [
                    "all"
                ], 
                "usedsize": ATLASDATADISK_USEDSIZE, 
                "vos": [
                    "atlas/Role=production"
                ], 
                "path": [
                    "/xrootd/atlas/atlasdatadisk"
                ]
            }, 
            {
                "name": "ATLASLOCALGROUPDISK", 
                "servingstate": "open", 
                "totalsize": ATLASLOCALGROUPDISK_TOTALSIZE, 
                "timestamp": TIMESTAMP,
                "assignedendpoints": [
                    "all"
                ], 
                "usedsize": ATLASLOCALGROUPDISK_USEDSIZE, 
                "vos": [
                    "atlas"
                ], 
                "path": [
                    "/xrootd/atlas/atlaslocalgroupdisk"
                ]
            }, 
            {
                "name": "ATLASSCRATCHDISK", 
                "servingstate": "open", 
                "totalsize": ATLASSCRATCHDISK_TOTALSIZE, 
                "timestamp": TIMESTAMP,
                "assignedendpoints": [
                    "all"
                ], 
                "usedsize": ATLASSCRATCHDISK_USEDSIZE, 
                "vos": [
                    "atlas"
                ], 
                "path": [
                    "/xrootd/atlas/atlas/atlasscratchdisk"
                ]
            }, 
            {
                "name": "DTEAM", 
                "servingstate": "open", 
                "totalsize": DTEAM_TOTALSIZE,
                "timestamp": TIMESTAMP,
                "assignedendpoints": [
                    "xrootd"
                ], 
                "usedsize": DTEAM_USERDSIZE, 
                "vos": [
                    "dteam"
                ], 
                "path": [
                    "/xrootd/atlas/tpctest"
                ]
            } 
        ] 
    }
}
```
