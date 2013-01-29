# -*- coding: utf-8 -*-

"""
MicroSAN Miscellaneous Module
"""

def get_int48(a):
    """
    Returns int48 from tuple
    """
    ret = 0
    for i in range(6):
        ret = (ret << 8) | a[i]
    return ret

