import socket
import psutil
import ipaddress
import os
import pathlib

UDP_PORT=5005
TCP_PORT=5006

bufferpath=os.path.join(os.environ.get('TEMP'), 'aircopybuffer')
outpath=os.path.join(os.environ.get('USERPROFILE'), 'Downloads', 'AirCopy')
pathlib.Path(outpath).mkdir(parents=True, exist_ok=True)


def calc_broadcast(ip, netmask):
	ip_int=int(ipaddress.IPv4Address(ip))
	netmask_int=int(ipaddress.IPv4Address(netmask))
	broadcast_int = ip_int | ~netmask_int & 0xFFFFFFFF
	broadcast_address = str(ipaddress.IPv4Address(broadcast_int))
	return broadcast_address

def get_baddr():
	baddr=[]
	for iface, addrs in psutil.net_if_addrs().items():
		for addr in addrs:
			if addr.family==socket.AF_INET:
				brd=calc_broadcast(addr.address, addr.netmask)
				#print(addr.address,' ',addr.netmask,' ',brd)
				baddr.append(brd)
				
	return [bcast for bcast in baddr if bcast]
	
def send_discovery():
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	baddr=get_baddr()
	for addr in baddr:
		sock.sendto('AIRCOPY_DISCOVERY'.encode(), (addr, UDP_PORT))
		
def recv_files():
	try:
		os.remove(bufferpath)
	except:
		pass
	try:
		sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(('0.0.0.0', TCP_PORT))
		sock.settimeout(10)
		sock.listen()
		send_discovery()
		print("Discovery sent")
		conn, addr = sock.accept()
	except:
		return
	currfile=open(bufferpath, 'wb')
	while True:
		data=conn.recv(1024)
		if not data:
			break
		currfile.write(data)
	sock.close()
	currfile.close()
	process_buffer()

def process_buffer():
	print('Received. Processing Buffer')
	begin='HEADERFL'
	end='COMPLETE'
	buf_file=open(bufferpath, 'rb')
	buf=buf_file.read()
	totlen=len(buf)
	i=0
	currfile=None
	while i<totlen:
		if buf[i:i+len(begin)]==begin.encode():
			i=i+len(begin)
			j=buf[i:i+3]
			fllen=int(j.decode())
			i=i+3
			filename=buf[i:i+fllen].decode()
			currfilepath=os.path.join(outpath, filename)
			currfile=open(currfilepath, 'wb')
			i=i+fllen
		elif buf[i:i+len(begin)]==end.encode():
			currfile.close()
			i=i+len(begin)
		else:
			currfile.write(bytes([buf[i]]))
			i=i+1
	buf_file.close()
	print("Processing complete")
	
