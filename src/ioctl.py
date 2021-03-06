# -*- coding: utf-8 -*-

from ctypes import *

def _IOW_BAD(type,nr,size): return _IOC(_IOC_WRITE,(type),(nr),sizeof(size)) # macro
def _IOR_BAD(type,nr,size): return _IOC(_IOC_READ,(type),(nr),sizeof(size)) # macro
def _IO(type,nr): return _IOC(_IOC_NONE,(type),(nr),0) # macro
def _IOC_SIZE(nr): return (((nr) >> _IOC_SIZESHIFT) & _IOC_SIZEMASK) # macro
def _IOW(type,nr,size): return _IOC(_IOC_WRITE,(type),(nr),(_IOC_TYPECHECK(size))) # macro
def _IOC_TYPE(nr): return (((nr) >> _IOC_TYPESHIFT) & _IOC_TYPEMASK) # macro
def _IOWR_BAD(type,nr,size): return _IOC(_IOC_READ|_IOC_WRITE,(type),(nr),sizeof(size)) # macro
def _IOC(dir,type,nr,size): return (((dir) << _IOC_DIRSHIFT) | ((type) << _IOC_TYPESHIFT) | ((nr) << _IOC_NRSHIFT) | ((size) << _IOC_SIZESHIFT)) # macro
def _IOC_DIR(nr): return (((nr) >> _IOC_DIRSHIFT) & _IOC_DIRMASK) # macro
def _IOWR(type,nr,size): return _IOC(_IOC_READ|_IOC_WRITE,(type),(nr),(_IOC_TYPECHECK(size))) # macro
def _IOC_TYPECHECK(t): return (sizeof(t)) # macro
def _IOR(type,nr,size): return _IOC(_IOC_READ,(type),(nr),(_IOC_TYPECHECK(size))) # macro
def _IOC_NR(nr): return (((nr) >> _IOC_NRSHIFT) & _IOC_NRMASK) # macro

_IOC_SIZESHIFT = 16 # Variable c_int '16'
_IOC_DIRBITS = 2 # Variable c_int '2'
_IOC_NRBITS = 8 # Variable c_int '8'
_IOC_SIZEBITS = 14 # Variable c_int '14'
IOCSIZE_SHIFT = 16 # Variable c_int '16'
IOC_IN = 1073741824L # Variable c_uint '1073741824'
_IOC_SIZEMASK = 16383 # Variable c_int '16383'
_IOC_WRITE = 1L # Variable c_uint '1'
_IOC_NRSHIFT = 0 # Variable c_int '0'
_IOC_TYPESHIFT = 8 # Variable c_int '8'
_IOC_DIRSHIFT = 30 # Variable c_int '30'
_IOC_TYPEMASK = 255 # Variable c_int '255'
_IOC_NRMASK = 255 # Variable c_int '255'
IOCSIZE_MASK = 1073676288 # Variable c_int '1073676288'
_IOC_READ = 2L # Variable c_uint '2'
_IOC_DIRMASK = 3 # Variable c_int '3'
_IOC_TYPEBITS = 8 # Variable c_int '8'
IOC_OUT = 2147483648L # Variable c_uint '2147483648'
IOC_INOUT = 3221225472L # Variable c_uint '3221225472'
_IOC_NONE = 0L # Variable c_uint '0'

__all__ = ['_IOC_DIRMASK', '_IOC_SIZEBITS', 'IOC_IN', '_IOC_NRSHIFT',
           '_IOC_TYPEBITS', '_IOC_DIRSHIFT', '_IOC_READ', 'IOC_OUT',
           '_IOC_DIR', '_IOC_NRBITS', '_IOC_WRITE', '_IOC_TYPESHIFT',
           '_IOC_TYPE', '_IOC_TYPECHECK', 'IOCSIZE_MASK', '_IOR_BAD',
           '_IOWR', '_IOC_NONE', '_IOC_SIZESHIFT', 'IOCSIZE_SHIFT',
           'IOC_INOUT', '_IOW', '_IOW_BAD', '_IOR', '_IOWR_BAD',
           '_IOC_TYPEMASK', '_IOC', '_IOC_NR', '_IOC_NRMASK',
           '_IOC_SIZE', '_IO', '_IOC_DIRBITS', '_IOC_SIZEMASK']
