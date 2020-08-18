import socket
import time

UDP_IP = "172.18.2.183"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
			socket.SOCK_DGRAM) # UDP
while True:
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	print "data sent to", UDP_IP
	time.sleep(20)
