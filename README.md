# vt_crawler
Use jquery to get the pronunciation challenge content of the voicetube service for the personal note.

# Config
1. You need to create a file for configure(include your accout and password).
# configure.py
```python
class Config:
    __email = '<your email>'
    __password = '<your password>'
    __remember = '1'
    def get_conf(self):
        return {
            'email': self.__email,
            'password': self.__password,
            'remember': self.__remember
        }
    def out_path(self):
        return {
            'my': '<your voice files path(depend on your disk)>',
            'host': '<host files path(depend on your disk)>'
        }
```
