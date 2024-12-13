import socket
import os

UDP_PORT=5005
TCP_PORT=5006

def pad_number(n):
	x=str(n)
	while len(x)<3:
		x='0'+x
	return x

def transfer(filelist):
	if len(filelist)==0:
		return
	print("Attempting to send ")
	for x in filelist:
		print(x)
	try:
		sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(('0.0.0.0', UDP_PORT))
		sock.settimeout(10)
		data,addr = sock.recvfrom(1024)
		print(addr)
		print(data)
		if data.decode()=='AIRCOPY_DISCOVERY':
			print("Discovery received")
		sock.close()
		client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((str(addr[0]), TCP_PORT))
		for file in filelist:
			if not os.path.isfile(file):
				continue
			filename=os.path.basename(file)
			print("Sending ", filename)
			header='HEADERFL'+pad_number(len(filename))+filename
			client.sendall(header.encode())
			currfile=open(file, 'rb')
			dat=currfile.read(1024)
			while(dat):
				client.send(dat)
				dat=currfile.read(1024)
			end='COMPLETE'
			client.send(end.encode())
		client.close()
	except:
		pass
