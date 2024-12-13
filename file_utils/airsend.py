import socket
import os

UDP_PORT=5005
TCP_PORT=5006


def transfer(filelist):
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('0.0.0.0', UDP_PORT))
	data,addr = sock.recvfrom(1024)
	print(data)
	if data.decode()=='AIRCOPY_DISCOVERY':
		print("Discovery received")
	sock.close()
	client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((addr, TCP_PORT))
	for file in filelist:
		filename=os.path.basename(file)
		print("Sending ", filename)
		header='HEADER'+filename
		client.sendall(header.encode())
		currfile=open(file, 'rb')
		dat=currfile.read(1024)
		while(dat):
			client.send(dat)
			dat=currfile.read(1024)
		end='COMPLETE'
		client.send(end.encode())
	client.close()