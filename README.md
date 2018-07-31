# vt_crawler
Use jquery to get the pronunciation challenge content of the voicetube service for the personal note.

## Config
1. You need to create a file for configure(include your accout and password).
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
    def out_path():
        return {
            'my': 'k:\/English_Study\/vt_notes\/others\/voice',
            'host': 'k:\/English_Study\/vt_notes\/others\/hosts'
        }
    @staticmethod
    def date_conf():
        return {
             'since': '20180802', # 開始日期
             'until': 2 # 持續天數
        }
```
