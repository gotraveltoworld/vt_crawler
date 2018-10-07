# vt_crawler
Use "requests" and "pyjquery" to get the pronunciation challenge content of the voicetube service for the personal note.

## Config
1. You need to create a file for configure(include your account and password).
2. You need to set your output path on your disk for the host's record, your record and the notes.
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
             'since': '20180802', # 開始日期
             'until': 2 # 持續天數
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
