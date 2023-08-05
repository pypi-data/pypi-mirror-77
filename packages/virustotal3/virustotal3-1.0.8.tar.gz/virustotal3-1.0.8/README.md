virustotal3
========
virustotal3 provides an easy way to use VirusTotal version 3 REST endpoints, including those exclusive to VirusTotal Enterprise such as Live Hunt, Retro Hunt and Zip Files that were not available in version 2.

### Changelog
#### 1.0.8
* Merged pull request #8

### Documentation
https://virustotal3.readthedocs.io/en/latest/

### Usage example
```
import os
import virustotal3.enterprise

API_KEY = os.environ['VT_API']

livehunt = virustotal3.enterprise.Livehunt(API_KEY)

rulesets = livehunt.get_rulesets()

print(rulesets)
```

Features
--------

- Access to many more features than the ones provided by the v2 API such as Live Hunt, Retro Hunt, Zip Files, Relationships, etc.
- Easy to use methods for all API endpoints (except Graphs).
- Simplified upload and download of files.
    - The API requires the use of a different endpoint for files larger than 32MB. the `File.upload()` method calculates the file size and picks the approriate endpoint.
- Written in Python 3.


Installation
------------
Installing with pip
`pip install virustotal3`

Install from repository
`python3 setup.py install`

Contribute
----------

- Issue Tracker: https://github.com/tr4cefl0w/virustotal3/issues
- Source Code: https://github.com/tr4cefl0w/virustotal3.git

Support
-------
The v3 API is in beta and under active development. While most of the implementation was tested and works perfectly, breaking changes might be introduced by VirusTotal. This rarely occurs, but recently URL.get_comments() and URL.get_votes() stopped working. An issue is current opened with VirusTotal (96772) and they are working on it.

If you are having issues, first make sure it does not come from the API itself. I'm in no way associated with VirusTotal. If it's an API bug, contact VirusTotal directly. Otherwise, open a GitHub issue.
