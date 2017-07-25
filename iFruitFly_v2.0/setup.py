from distutils.core import setup
import py2exe
import sys
import numpy

sys.setrecursionlimit(1000000000)


#setup(console=['testingCommandLine.py'])
setup(
    options = {
            "py2exe":{"dll_excludes": ["HID.DLL", "w9xpopen.exe", "hdf5.dll", "libzmq.pyd"], }}, console = [{'script': 'testingCommandLine.py'}]
)