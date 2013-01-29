# -*- coding: utf-8 -*-

"""
MicroSAN Main module
"""

from proto import uSanProto
from network import BroadcastSocket, UDPSocket, MICROSAN_PORT
from nbd import *

import sys, os
import fcntl

class App(object):
    """
    Application class
    """
    _active_socket = None

    def __init__(self):
        """
        Constructor
        """
        pass

    def _find_roots(self):
        """
        Retrieves root disks
        """
        print "Finding root disks..."

        # Query MicroSAN disks
        fd_pkt = uSanProto.FindDisks()

        # Send packet
        bs = BroadcastSocket()
        bs.send_data(fd_pkt)
        while True:
            try:
                bs.recv_data()
            except:
                break

        bs.close()

        # Parse root disks
        disks = []
        for reply_info in bs.buf:
            pkt = reply_info[0]
            addr = reply_info[1]
            pkt_data = uSanProto.FindDisks.parse_reply(pkt)
            ipaddr = pkt_data[0]
            print 'Found root disk: %s' % ipaddr
            disks.append(ipaddr)

        return disks

    def _info_roots(self, disks):
        """
        Queries root disks for information
        """
        us = UDPSocket()

        disk_info = {}
        for disk in disks:
            # Create packet and sent it
            qd_pkt = uSanProto.Disks.query(disk)
            qaddr = (disk, MICROSAN_PORT)
            us.send_data(qd_pkt, qaddr)
            while True:
                try:
                    us.recv_data()
                except:
                    break

            # We've got reply
            replies = us.buf
            us.clear_buf()

            # Parse replies
            for reply_info in replies:
                qd_rpkt = reply_info[0]
                qr_data = uSanProto.Disks.parse_query_reply(qd_rpkt)
                disk_data = uSanProto.Disks.parse_disk_info(qr_data[3])

                disk_info[disk] = disk_data

        us.close()

        return disk_info

    def _get_parts(self, disk, parts):
        """
        Queries partitions info
        """
        us = UDPSocket()

        part_infos = []
        for part_num in range(1, parts + 1):
            qp_pkt = uSanProto.Partitions.query_root(disk, part_num)
            qaddr = (disk, MICROSAN_PORT)
            us.send_data(qp_pkt, qaddr)
            while True:
                try:
                    us.recv_data()
                except:
                    break

            part_infos.extend(us.buf)
            us.clear_buf()

        us.close()

        return part_infos

    def _info_parts(self, disk_parts):
        """
        Queries partitions for information
        """
        part_infos = {}
        for disk, part_pkt in disk_parts.items():
            part_infos[disk] = []
            for part_info in part_pkt:
                part_data = uSanProto.Partitions.parse_root_info(part_info[0])
                part_infos[disk].append(part_data)

        return part_infos

    def _ipaddr_part(self, parts_info):
        """
        Resolves ip address for partition
        """
        part_ipaddr = {}
        for disk, parts in parts_info.items():
            rp_replies = []
            part_ipaddr[disk] = []
            for part_info in parts:
                part_id = part_info[2]
                rp_reply_data = self.name_res(part_id)
                part_ipaddr[disk].append(rp_reply_data)

        return part_ipaddr

    def _show_roots_info(self, roots_info, parts_info, parts_ipaddr):
        """
        Shows roots info
        """
        keys = roots_info.keys()
        keys.sort()

        for disk in keys:
            info = roots_info[disk]
            print 'Root disk %s (%s) has %d partitions' % (disk, info[7], info[6])
            print '\tMarket Class=%s, Manufacturer code=%s, Part no.=%s' % (info[1], info[2], info[3])

        for disk in keys:
            info = roots_info[disk]
            total_size = info[4] / (1024 * 1024)
            free_size = info[5] / (1024 * 1024)
            print '=' * 80
            print 'VERSION  : %-30s ROOT IP ADDR: %-15s' % (info[0], disk)
            print 'TOTAL(MB): %-30d # PARTITIONS: %-d' % (total_size, info[6])
            print 'FREE (MB): %-30d' % (free_size)

            if len(parts_info[disk]) > 0:
                print '- ' * 40
                print 'PARTITION%36sLABEL%8sIP ADDR%5sSIZE (MB)\n' % ('', '', '')

                i = 0
                for part_info in parts_info[disk]:
                    part_label = part_info[0]
                    part_size = part_info[1] / (1024 * 1024)
                    part_id = part_info[2]
                    part_ipaddr = parts_ipaddr[disk][i][1]
                    print '%- 44s %- 10s %- 15s %6d' % (part_id, part_label, part_ipaddr, part_size)
                    i += 1

    def _query_part(self, part_ipaddr):
        """
        Queries partition information by ip address
        """
        us = UDPSocket()

        qp_pkt = uSanProto.Partitions.query_part()
        qaddr = (part_ipaddr, MICROSAN_PORT)
        us.send_data(qp_pkt, qaddr)
        while True:
            try:
                us.recv_data()
            except:
                break

        part_info = us.buf
        us.close()

        return part_info


    def list_all(self):
        """
        Lists all disks and partitions
        """
        disks = self._find_roots()
        disks_info = self._info_roots(disks)

        disk_parts = {}
        for disk, disk_info in disks_info.items():
            parts = disk_info[6]
            disk_parts[disk] = self._get_parts(disk, parts)

        parts_info = self._info_parts(disk_parts)
        # FIXME: Fix when bad data returned
        parts_ipaddr = self._ipaddr_part(parts_info)

        self._show_roots_info(disks_info, parts_info, parts_ipaddr)

    def name_res(self, uid):
        """
        Resolve partition IP address by UID
        """
        bs = BroadcastSocket()

        rp_pkt = uSanProto.Resolve(uid)
        bs.send_data(rp_pkt)

        while True:
            try:
                bs.recv_data()
            except:
                break

        rp_reply = bs.buf[0]
        bs.close()

        rp_reply_data = uSanProto.Resolve.parse(rp_reply[0])

        return rp_reply_data

#    def read(self, part_id, offset):
#        """
#        Reads data part_id from offset
#        """

    def attach(self, part_id, path):
        """
        Attaches MicroSAN as Network Block Device
        """
        # Open NBD device
        nbd_fd = os.open(path, os.O_RDWR)

        # Set kernel parameters for NBD
        sysfs_name = '/sys/block/%s/queue/max_sectors_kb' % os.path.basename(path)
        sysfs = os.open(sysfs_name, os.O_RDWR)
        os.write(sysfs, '8')
        os.close(sysfs)

        # Resolve partition ip address
        part_ipaddr = self.name_res(part_id)[1]
        # Get partition information
        part_info = self._query_part(part_ipaddr)[0]
        # Parse partition information
        part_data = uSanProto.Partitions.parse_root_info(part_info[0])
        part_size = part_data[1]

        # Size of blocks (12 = 4KB block)
        block_size_power = 12
        block_size = part_size >> block_size_power

        # Set block sizes on device
        ioc = fcntl.ioctl(nbd_fd, NBD_SET_BLKSIZE, long(1 << block_size_power))
        if ioc < 0:
            raise IOError('nbd_fd cannot set NBD_SET_BLKSIZE')

        ioc = fcntl.ioctl(nbd_fd, NBD_SET_SIZE_BLOCKS, block_size)
        if ioc < 0:
            raise IOError('nbd_fd cannot set NBD_SET_SIZE_BLOCKS')
        
        






app = App()
app.list_all()
#app.name_res('7F963218-5075-11D8-9BF9-00508DE39365')
#app.attach('7F963218-5075-11D8-9BF9-00508DE39365', '/dev/nbd0')
