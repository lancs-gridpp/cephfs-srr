# cephfs-srr

These scripts return a SRR JSON file containing information about the endpoints and storage mounted using CephFS.  It uses *ceph.quota.max_bytes* and *ceph.dir.rbytes* to get available and used space details.

The latest version of the Storage Resource Reporting proposal can be found here:  
https://docs.google.com/document/d/1yzCvKpxsbcQC5K9MyvXc-vBF1HGPBk4vhjw3MEXoXf8/edit 


## Installation

The installation has changed. Installation can now be done using pip

 * Download the source.  Either clone https://github.com/lancs-gridpp/cephfs-srr.git or download and extract the *.tar.gz* file from the */dist* directory.
 * In the root directory of the source, run the following command as the user that will run the storage_summary script.
   This will install the cephfs-srr python package and place the ``storage_summary`` script in the system PATH.
   
 ```
 $ pip3 install .
 ```

  * You can verify the installation with

 ```
 $ which storage_summary
 ```
 
 
 * Copy cephsrr.conf to /etc and edit. See: [Configuration File - cephsrr.conf](#Configuration File - cephsrr.conf)
 
### Python Setup Tools

Older versions of python/setuptools do not support using a *.toml* file so a setup.py has also been included.

You can update your setup tools with:
```
$ pip3 install --upgrade setuptools
```

### Building Distribution .tar.gz and Wheel

To build a package *.tar.gz* and wheel run

```
$ python3 -m build
```

This will create the *dist* directory containing .tar.gz* and *.whl* files.
 
## Uninstalling
To remove the executable script *storage_summary* and the python package cephfs_srr run:

```
$ pip3 uninstall cephfs_srr
```


## Upgrading from V1.0
> [!NOTE]
> Because of the change to the installation procedure, there has been a name change from *storage-summary.py* to *storage_summary*.

If you are running version 1.0 you need to manually remove  ```/usr/share/cephsrr``` and the link in ```/usr/bin``` to ```storage-summary.py``

Either clone https://github.com/lancs-gridpp/cephfs-srr.git or download and extract the tar.gz file from the dist directory.
 * In the source root directory, run the following as the user that will run the storage_summary script. 
   This will install the cephfs-srr python package and place the ```storage_summary``` script in the system PATH.  
   
 ```
 pip3 install .
 ```
 
There are some extra configuration settings that will need adding to the cephsrr.conf
```
    [default]
    implementation = xrootd_cephfs
    implementationversion = 
    qualitylevel = production
```

*implementationversion* will need setting to your version of xrootd.
 
## Building Distribution Files

Run the following command in the source root directory.

```
$ python3 -m build
```

This will create a *.tar.gz* file and a *.whl* file in the *dist* directory. 

If you need to add extra files to the distribution files, add them into the *MANIFEST.in* file.

## Configuration File - cephsrr.conf
There are 3 section types in the configuration file: default, endpoint and share.  

### Default Section
There should only be one default section defined.

```
[default]
    hostname = fal-pygrid-30.lancs.ac.uk
    srroutput = /storage/srr.json
    logginglevel = info
    implementation = xrootd_cephfs
    qualitylevel = production
```
 * **hostname** is optional. The machines hostname is used if not specified here.
 * **srroutput** specifies where the output JSON should be written to.  If this is excluded the output will go to stdout.
 * **logginglevel** specifies the level of logging output. The options are: debug, info, warning, error, critical.
 * **implementation** Text output in the json.
 * **qualitylevel** Text output in the json.

### Endpoint Sections

There can be more than one endpoint section.  Each section must have a unique name and start with *\[endpoint*. The text after *\[endpoint* and before *\]* is ignored.

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

## Logging 
*storage_summary* logs to */dev/log*. The level of logging can be set using the cephsrr.conf file. 

```
[default]
    # Level of logging: debug, info, warning, error, critical
    logginglevel = info
```


## Example SRR

https://twiki.cern.ch/twiki/pub/LCG/StorageSpaceAccounting/xrootd.srr.slac.json

```
{
    "storageservice": {
        "datastores": [], 
        "latestupdate": TIMESTAMP,
        "name": "slac.stanford.edu", 
        "implementation": "xrootd-ceph", 
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


