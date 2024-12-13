import socket
import psutil
import ipaddress

UDP_PORT=5005
TCP_PORT=5006

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
	sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('0.0.0.0', TCP_PORT))
	sock.listen()
	send_discovery()
	conn, addr = s.accept()
	currfile=None
	while True:
		data=conn.recv(1024)
		if not data:
			break
		begin='HEADER'
		end='COMPLETE'
		header_flag=False
		end_flag=False
		if data[:len(begin)]==begin.encode():
			header_flag=True
			filename=data[len(begin):].decode()
			currfile=open(filename, 'wb')
		elif data[:len(end)]==end.encode():
			end_flag=True
			currfile.close()
		else:
			currfile.write(data)
	sock.close()
	

