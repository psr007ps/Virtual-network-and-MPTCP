# Virtual-network-and-MPTCP
A virtual network on local machine and performance test of multipath-TCP.

Contents:

MPTCP setup using mininet

Create a topology

Does MPTCP improve file transfer performance? 

Does MPTCP improve (approximated) web browsing performance?



Handy commands

 Check all available interfaces: ifconfig -a

 Enable interface eth0: ifconfig eth0 up

 Check current routing: route -n or ip route show

 Analyze network traffic: wireshark

 Run a simple web server: python -m SimpleHTTPServer 80

 Limit outgoing rate on eth0 interface: tc qdisc add dev eth0 root tbf
rate 1mbit burst 1mbit latency 1ms

 Time webpage download time time wget -pq --no-cache --deleteafter www.cnn.com
Mininet-specific commands (run from Mininet)

 Ping between hosts h1 and h2: h1 ping h2

 Any command you want to send to host h1: h1 <command>

 Open up a new terminal for host h1: xterm h1

Mininet topology configuration (e.g., in linuxrouter.py)

• Run a command on h2: net['h2'].cmd('ip rule add from 10.0.2.100 table 1')

• Set the IP address of a specific interface on h2:

net['h2'].setIP('10.0.3.100/24',intf='h2-eth1')
