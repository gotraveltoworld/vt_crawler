# vt_crawler
Use "requests" and "pyquery" to get the pronunciation challenge content of the voicetube service for the personal note.

### Update records
1. Delete the "pyquery" library.
2. Only use the "requests" to build simple crawler.
3. Fix some of bugs about the mkdir function.

## Config
1. You have to create a file for configure(include your account and password), to add 'configure.py' file.
2. You have to set your output path on your disk for the record of a host, your record and the notes.
3. You can add below script into the 'configure.py'.

#### configure.py
```python
class Config:
    @staticmethod
    def get_conf():
        return {
            'email': '<your email>',
            'password': '<your password>',
            'remember': '1'
        }
    @staticmethod
    def other_cookie():
        return {
            'vt-origin': '1' # Keep the page of the original version.
        }
    @staticmethod
    def out_path():
        return {
            'notes': '<your note files path on your disk>',
            'my': '<your voice files path(depend on your disk)>',
            'host': '<host files path(depend on your disk)>'
        }
    @staticmethod
    def date_conf():
        return {
             'since': '20180802', # Start date
             'until': 2 # continue days
        }
```
### Run download
Use the sync script to download the notes from the web page.
```
python vt_crawler.py
```
## New feature
Use the asyncio to download the notes from the web page.
```
python async_vt_crawler.py
```
