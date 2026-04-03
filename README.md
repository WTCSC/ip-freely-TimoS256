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
