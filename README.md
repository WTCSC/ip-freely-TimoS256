# IP-Freely
IP Freely is a simple network scanning tool. <br>
It works by running ping on every ip address in the range of the ip address you pass it. <br>
<br>
## Installation and Usage
Clone the repo
```
git clone github.com/WTCSC/ip-freely-TimoS256
cd ip-freely-TimoS256
sudo python3 main.py
```
With sudo permissions, run main.py, and specify the ip with --ip. CIDR Notation is required.
```
sudo python3 main.py --ip 192.168.0.0/24
```
### Port Scanning
IP Freely now has port scanning functionality, this lets you check the status and service of a specified port or list of ports.
##### Syntax
--pt port
<br>
port can be a single number, a set of numbers seperated by commas, or a range, indicated by two numbers hyphenated.
```
--pt 80
--pt 22,80,443
--pt 22-443
```
##### Examples
```
sudo python3 main.py --ip 192.168.0.0/24 --pt 22
```
Scans the network, checks if port 22 is open on any accessible ip addresses
```
sudo python3 main.py --ip 192.168.0.100/24 --pt 22,80,443
```
Same as before, but checks 22, 80 and 443
```
sudo python3 main.py --ip 192.168.0.100/24 --pt 1-1000
```
Scans for every port between 1 and 1000, only prints open ports to avoid flooding your terminal.
