import sys
from socket import SOL_SOCKET, SO_BROADCAST

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import task
from twisted.python import log

log.startLogging(sys.stdout)

port = 20001

class BroadcastingDatagramProtocol(protocol.DatagramProtocol):

  port = port

  def startProtocol(self):
    self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
    self.call = task.LoopingCall(self.tick)
    self.dcall = self.call.start(1.0)

  def stopProtocol(self):
    self.call.stop()

  def tick(self):
    self.transport.write(self.getPacket(), ("<broadcast>", self.port))

  def getPacket(self):
    return "Some bytes for you"

  def datagramReceived(self, data, addr):
    print "Received", repr(data)

reactor.listenUDP(port, BroadcastingDatagramProtocol())
reactor.run()
