## [1.1.0] - 2025-02-25

### Added
* The following addtional config options have been added.  If the settings are not added to the cephsrr.conf, the values shown below will be used by default. *implementationversion* will need setting to your version of xrootd.
    ```
    [default]
    implementation = xrootd_cephfs
    implementationversion = 
    qualitylevel = production
    ```
* Added files to allow installing/uninstalling using pip3. 

### Changed
* Changed the packaging (sorry) so it can be installed using *pip3*. The *cephfs_srr* package is installed and the runnable script *storage_summary* in the PATH .  
* **The change in packaging has meant a name change from *storage-summary* to *storage_summary*.**
* The main python files have been moved to the *cephfs_srr* directory and *storage_summary.cgi* is now in the *cgi-run* directory.  
