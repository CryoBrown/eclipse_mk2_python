import socket
import json

import optparse

parser = optparse.OptionParser()

parser.add_option('--s', action="store", dest="server", help="ip address", default = "127.0.0.1")
parser.add_option('--c', action="store", dest="client", help="ip address", default = "127.0.0.1")
options, args = parser.parse_args()
print "SERVER IP:", options.server
print "CLIENT IP:", options.client

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address_me = (options.server, 5004)
address_u = (options.client, 5005)
serversocket.bind(address_me)

#code for socket.SOCK_STREAM
#serversocket.listen(1) # become a server socket, maximum 1 connections
#connection, address = serversocket.accept()

i = 0
while True:
        print "----------------------------------------------"
        print "BEGIN LOOP " + str(i)

        dic = {'load' : 0.0, 'pressure' : 0.0, 'thermo' : 0.0}
        data = json.dumps(dic)

        print "DATA:"
        print data
        print "SENDING..."
        serversocket.sendto(data, address_u)
        #connection.send(data)
        print "done."
        print "\n\n"

        print "RECEIVING..."
        received, addr = serversocket.recvfrom(1024)
        #received = connection.recv(1024)
        print "done."
        print "RECEIVED:"
        print received
        print "\n\n"
        stats = json.loads(received)

        print "END LOOP " + str(i)
        print "----------------------------------------------\n"
        i+=1