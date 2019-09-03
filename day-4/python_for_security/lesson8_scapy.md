# **Scapy** Packet Analysis in Python Made Easy
----
Scapy is an open source python project that allows us to send, build, decode, sniff, and dissect network packets. 

With this capability we can explore network traffic and execute attacks.

scapy has a few methods in it that let learning how to use it and starting an anlysis easy

use `ls()` to list the layers

use `lsc()` to list the commands

**Packet Sniffing with Scapy**
Raw sockets can  be a pain to set up and are not too portable across Operating Systems

there are a majority of libraries out there to use
* `pylibpcap`
* `pycapy`
* `impacket`
* `scapy`

**Scapy** offers an interactive mode or use of the library in a project.

it can be used for packet sniffing and forgery, has tons of protocols built into it and allows you to build _reactive_ tools 

**Protocol Layers Available**
* `ls()`
* `ls(IP)`
* `IP().show()`
* `lsc()`
* `conf`

## **Sniffing with Scapy**:
----

With the `sniff()`` we can sniff traffic. 

`help('sniff()')` is worth a quick read. 

`sniff(iface="eth0", filter = "icmp",count="10")` will make a `pcap` file

you can call the `summary()` or `nsummary()` to display the results

with all of the packets, scapy can be used to explore the information that the packet returns. 

to dig deeper into an individual packet 

```python
P = sniff()
p.nsummary()
p.summary()

p[numberOfPacket] # will display the selected packet info
p[numberOfPacket][UDP].dport # dig into the selected packet
```

you can declare a variable to hold all of the packets

`pkts = sniff(iface="eth1",count=3)

pkts # will show you the sniff status
pkts[0]
pkts[1]
pkts[2]
hexdump(pkts[1]) #will show you the data in HEX form
```

There is also an ability to add Filters into the dump

```python
pkts = sniff(iface="eth1", filter="arp",count=3) # will filter for icmp traffic of pings
#write packets to the pcap file
wrpcap("test.cap", pkts)

#read from the pcap file
rdpcap("test.cap")

icmp_str = str(pkts[0])  # this will make the packet string
export_object(icmp_str)  # this would show a Base64 encoded packet
newPacket = import_object() # now the packet will listen for Base64 encoded Data

## Build a packet

IcmpPacket:
    send(IP(dst="10.0.0.138")/ICMP("data")

#you can spoof the ip address by adding a source IP

send(IP(dst="10.0.0.138",src="10.0.0.8")/ICMP("data"))
```

## **Sending and Receiving**:
----

**Layer 3 packets (IP, ARP, etc)**:

**send()** send one packet into layer 3
**Ans, unans = sr()** sending packets and receiving answers
**sr1()** this function only returns one packet answering the sent packet

**layer 2 (ethernet, 802.3, etc.)**:

**sendp()** send one packet in layer 2
**srp()** like sr() for layer 2

## **Scanning**:
----

`sr(dst="10.0.0.138")/TCP(dport=[21,22,23,80], flags="S")`

### **Exercise**:
----
1. Create a packet sniffer with scapy for HTTP protocols and print out
* The HTTP HEaders
* The data in the GET/POST

2. Create a Wi-Fi Sniffer and print out unique SSDs of the Wifi Network


## **Packet Injection with Scapy**:
----
|Ethernet|IP|TCP|Application|
|Ether()|IP()|TCP()|DATA|

`pkt = IP(dst="google.com")` this will show you the packet information from google.com `pkt.show()`

**Send packets with scapy**
* `sendp` send packets at layer 2, needs to give the right interface as an argument
* `send` send packets at layer 3, routing decided based on local tables
    * loop on the same packet
    * inter: time intervals

**Outside of Layer 3** you need to tell scapy which layer to use

run `tcpdump -i eth1 -XX -vv icmp` in the background ( using `&` ) to catch the right packets

**Sending with Layer 3:**
----
```python
pkt = IP(dst="google.com")/ICMP()/"Python Class"

send(pkt)
```
checking `tcpdump` will show you if you collected the right packet

**Sending with Layer 2:** 
---- 
`sendp(Ether()/IP(dst="google.com")/ICMP()/"XXX", iface="eth1")`

you can loop sending many packets with

`sendp(Ether()/IP(dst="google.com")/ICMP()/"XXX", iface="eth1", loop=1)`
use `CTRL + C` to kill the commands

you can also set an interval for 1 second
`sendp(Ether()/IP(dst="google.com")/ICMP()/"XXX", iface="eth1", loop=1, inter=1)`
use `CTRL + C` to kill the commands

**Send and Receive at Layer 2 and 3:**
----
For Layer 3 use:
`sr()` will return answered and unanswerd packets

`sr1()` will return only answered or sent packets

For Layer 2:
`srp()` and `srp1()`

**send and receive with scapy**

`sr(IP(dst="google.com")/ICMP()/"XXX")`

`reponse, no_reponse = _` This will store the latest evaluations result

`response[0]` will give you the information for the packet that responded

if you know you need to wait for an aswer you can use the `timout` arugment 
    `sr(IP(dst="google.com"), timeout=5)`
`sr1()` will stop waiting automatically

**Routing with Scapy**

`conf.route` will show you the routing table of your computer

`conf.route.add(host="10.0.0.2", gw="10.0.0.11") #this wont change the table on all machines
This will make so that packets for `10.0.0.2` will use the new `10.0.0.6` check it with `conf.route`

you can change all the networks routing with scapy using 
`conf.route.add(net="10.0.0.1/8", gw="10.0.0.11")`

`conf.route.resync()` will remove all the new settings you made

## **Injected Packet Rounting**
---

Packet injecting with scapy will use the local routes, be default. This can be overridden with scapy.
Modified routes can be flushed. It will not affect system routes. 

**Progamming with Scapy**:

```python
from scapy.all import Ether, IP, TCP, sr1

#import all with scapy
# you can also use scapy.all import *

the `ls(ARP)` command with check for all ARP options

```python 

for lsb in range (1,50):
    ip = "10.0.0."+str(lsb)
    arpRequest = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
    arpRequest = srp1(arpRequest, timeout=1, verbose=0)

    if arpResponse:
        print "IP: " + arpResponse.psrc + "MAC: " + arpResponse.hwsrc
```

## **Exercises**:
----
1. Write a script that will take from the user a number of packets to sniff and capture the traffic

2. Explore packet number 6, what is the source port? what is the destination port?

3. How can you perform an arp scan to you network (e.g. 10.0.0.*)?

4. Run the command "traceroute('google.com')" what does packet number 11 mean?

5. Scan facebook.com  using scapy. which ports are open?

6. Find you local subnet automatically

7. Create a DNS poisoning tool similar to DNSSpoof using Scapy

8. Create an ARP MITM tool using Scapy

9. Create a TCP SYN Scanner using Scapy

10. Read about fuzzers
