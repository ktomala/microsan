# -*- coding: utf-8 -*-

from ioctl import _IO

NBD_SET_SOCK = _IO( 0xab, 0 )
NBD_SET_BLKSIZE = _IO( 0xab, 1 )
NBD_SET_SIZE = _IO( 0xab, 2 )
NBD_DO_IT = _IO( 0xab, 3 )
NBD_CLEAR_SOCK = _IO( 0xab, 4 )
NBD_CLEAR_QUE = _IO( 0xab, 5 )
NBD_PRINT_DEBUG = _IO( 0xab, 6 )
NBD_SET_SIZE_BLOCKS = _IO( 0xab, 7 )
NBD_DISCONNECT = _IO( 0xab, 8 )
NBD_SET_TIMEOUT = _IO( 0xab, 9 )

NBD_CMD_READ = 0
NBD_CMD_WRITE = 1
NBD_CMD_DISC = 2
NBD_REPLY_MAGIC = 1732535960
NBD_REQUEST_MAGIC = 627086611
