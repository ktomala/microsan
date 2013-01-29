# -*- coding: utf-8 -*-

"""
MicroSAN Protocol Module
"""

import random
import time
import struct
import os
import socket

from misc import get_int48

USAN_PROTO_FIND = 0x0d
USAN_PROTO_FIND_REPLY = 0x0e
USAN_PROTO_GET = 0x00
USAN_PROTO_GET_REPLY = 0x11
USAN_PROTO_RESOLVE = 0x0f
USAN_PROTO_RESOLVE_REPLY = 0x10
USAN_PROTO_PUT = 0x01
USAN_PROTO_PUT_REPLY = 0x04
USAN_PROTO_IDENTIFY = 0x13

class uSanNextSeq(object):
    """
    MicroSAN next sequence class
    """
    seq = 1 << 15

    @classmethod
    def __new__(uSanNextSeq, cls):
        if cls.seq & (1 << 15):
            random.seed(int(time.time()) ^ os.getpid())
            cls.seq = random.randint(0, 1 << 15) % (1 << 15)

        cls.seq += 1

        if cls.seq & (1 << 15):
            cls.seq = 0

        return cls.seq

class uSanProto(object):
    """
    MicroSAN protocol class
    """

    class Control(object):
        """
        Protocol control (core)
        """

        @staticmethod
        def __new__(cls, cmd, len_power = 0, seq = uSanNextSeq()):
            """
            int8 - cmd
            int8 - len_power
            int16 - seq
            """
            fmt = '2bh'
            return struct.pack(fmt, cmd, len_power, seq)

        @staticmethod
        def parse(packet):
            """
            Parses packet data
            """
            fmt = '2bh'
            cmd, len_power, seq = struct.unpack(fmt, packet[:4])
            if len(packet) > 4:
                data = packet[4:]
            else:
                data = None
            return (cmd, len_power, seq, data)

    class Get(object):
        """
        Get method class
        """

        @staticmethod
        def __new__(cls, disk, sector = 0, info = 1, add_info = ''):
            """
            Creates Get method packet

            int8[12] - unknown
            int8[4] - ip address
            int8[2] - unknown
            int32 - sector
            int8 - unknown
            int8 - info
            """
            ctrl = uSanProto.Control(USAN_PROTO_GET, len_power = 9)
            ipaddr = socket.inet_pton(socket.AF_INET, disk)
            sector = struct.pack('>i', sector)
            info = struct.pack('b', info)
            pkt = ''.join([ctrl, 12 * '\x00', ipaddr, 2 * '\x00', sector, '\x00', info, add_info])
            return pkt

        @staticmethod
        def parse(data):
            """
            Parses get method
            """
            ipaddr = socket.inet_ntop(socket.AF_INET, data[12:16])
            if len(data) > 16:
                sector = struct.unpack('i', data[18:22])[0]
                info = struct.unpack('b', data[24])[0]
            else:
                sector = None
                info = None
            if len(data) > 24:
                add_info = data[24:]
            else:
                add_info = None
            return (ipaddr, sector, info, add_info)

    class Resolve(object):
        """
        Resolve method class
        """

        @staticmethod
        def __new__(cls, part_id):
            """
            Creates Resolve method packet
            """
            ctrl = uSanProto.Control(USAN_PROTO_RESOLVE)
            part_id = struct.pack('64s', part_id)
            pkt = ''.join([ctrl, part_id])
            return pkt

        @staticmethod
        def parse(pkt):
            """
            Parses Resolve reply packet

            char[64] - partition id
            int8[12] - unknown
            int8[4] - ip address
            int8[20] - unknown
            """
            reply = uSanProto.Control.parse(pkt)
            resolve_data = reply[3]

            part_id = struct.unpack('64s', resolve_data[:64])[0]
            ipaddr = socket.inet_ntop(socket.AF_INET, resolve_data[76:80])

            return (part_id, ipaddr)


    class FindDisks(object):
        """
        Finds disks
        """

        @staticmethod
        def __new__(cls):
            """
            Creates find_disks packet
            """
            pkt = uSanProto.Control(USAN_PROTO_FIND)
            return pkt

        @staticmethod
        def parse_reply(pkt):
            """
            Parses reply

            int8[12] - unknown
            int8[4] - ip address
            """
            reply = uSanProto.Control.parse(pkt)
            data = reply[3]
            get_data = uSanProto.Get.parse(data)
            return get_data

    class Disks(object):
        """
        Disks operations
        """

        @staticmethod
        def query(disk):
            """
            Queries disk
            """
            add_info = '\x52\x20\x20\x20'
            pkt = uSanProto.Get(disk, sector = 0, info = 1, add_info = add_info)
            return pkt

        @staticmethod
        def parse_query_reply(pkt):
            """
            Parses reply
            """
            reply = uSanProto.Control.parse(pkt)
            data = reply[3]
            get_data = uSanProto.Get.parse(data)
            return get_data

        @staticmethod
        def parse_disk_info(disk_data):
            """
            Parses partition data
            """
            version = struct.unpack('16s', disk_data[:16])[0]
            market_class = struct.unpack('2B', disk_data[16:18])
            manufacturer = struct.unpack('3B', disk_data[18:21])
            part_no = struct.unpack('3B', disk_data[21:24])
            sector_total = struct.unpack('6B', disk_data[24:30])
            sector_free = struct.unpack('6B', disk_data[30:36])
            partitions = struct.unpack('B', disk_data[41])[0]
            label = struct.unpack('56s', disk_data[46:102])[0]

            # Convert strings
            version = version.replace('\x00', '').strip()
            label = label.replace('\x00', '').strip()

            # Convert sizes to proper number of bytes
            sector_total = get_int48(sector_total) << 9
            sector_free = get_int48(sector_free) << 9

            return (version, market_class, manufacturer, part_no, sector_total, sector_free, partitions, label)

    class Partitions(object):
        """
        Partitions operations
        """

        @staticmethod
        def query_root(disk, partition):
            """
            Queries root disk
            """
            add_info = '\x52\x20\x20\x20'
            pkt = uSanProto.Get(disk, sector = partition, info = 1, add_info = add_info)
            return pkt

        @staticmethod
        def parse_root_info(pkt):
            """
            Parses root info
            """
            get_data = uSanProto.Disks.parse_query_reply(pkt)
            root_data = get_data[3]

            label = struct.unpack('28s', root_data[6:34])[0]
            sector_size = struct.unpack('6B', root_data[134:140])
            part_id = struct.unpack('64s', root_data[178:242])[0]

            label = label.replace('\x00', '').strip()
            part_id = part_id.replace('\x00', '').strip()

            sector_size = get_int48(sector_size) << 9

            return (label, sector_size, part_id)

        @staticmethod
        def query_part():
            """
            Queries partition
            """
            add_info = '\x52\x20\x20\x20'
            ctrl = uSanProto.Control(USAN_PROTO_IDENTIFY, len_power = 9)
            pkt = ''.join([ctrl, 24 * '\x00'])
            return pkt
