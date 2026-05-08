import pythonping as p
import click
import csv
import socket

#Setup the output to csv
fields = ['ID','IP','Result','Hostname']
rows = []

#Setup the cli via click
@click.command()
@click.option('--ip', help="the IP range to be scanned")
@click.option('--pt', help="ports to be scanned")


def scan(ip,pt):
    print(ip)
    ips = getrange(ip)
    out = []
    h = 0
    for x in ips:
        h += 1
        print(f'\n -----   {x}')
        print(f'#{h}')
        result = ping(x)
        print(result)
        host = lookup(x,pt)
        print(f'DNS: {host}')
        #Puts all the outputs in a list to be added to the out list as a matrix, to go into the csv file
        out = [h,x,result,host]
        rows.append(out)
    print(rows)
    write()
def ping(ip):
        result =  p.ping(ip, verbose=True, count=1, timeout=0.5)
        if result.success():
            return '---- Passed! ----'
        else:
            return "Failed :("
def lookup(ip,pt):
    try:
        r = socket.gethostbyaddr(ip)
        if not pt == None:
            portscan(ip,pt)
        return r
    except:
        return "Failed"
def portparse(ports: str) -> list[int]:
    ports = ports.strip()

    if '-' in ports and ',' not in ports:
        start,end = ports.split('-')
        return list(range(int(start),int(end)+1))
    return [int(p.strip()) for p in ports.split(',')]
def portcheck(ip,port):
    timeout = 1.0
    try:
        with socket.create_connection((ip,port), timeout=timeout):
            return port, True
    except:
        return port, False

def get_service(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"
    
def portscan(ip,pt):
    print('-- portscanning --')
    ports = portparse(pt)
    for x in ports:
        portISOpen = portcheck(ip,x)
        if portISOpen[1] == True:
            print(f'>Port {x} is Open ({get_service(x)})')
def write():
    #write output to csv file
    with open('results.csv', 'w') as csvf:
        csvwriter = csv.writer(csvf)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def getrange(ip_in):
    ip, cidr = ip_in.split('/')
    host_bits = 32 - int(cidr)
    count = 2 ** host_bits
    range_out = []
    # split the ip into octets
    octs = []
    for x in ip.split('.'):
        octs.append(int(x))
    #Reconstruct the octets into an int
    ip_int = (octs[0] << 24) | (octs[1] << 16) | (octs[2] << 8) | octs[3]

    #Find the subnet mask by creating 32 1s and pushing them out by the amount specified in cidr notation
    subnet = (0xFFFFFFFF << host_bits) & 0xFFFFFFFF
    #get the lowest ip by combining the first section of the ip with the mask, so only the part we iterate through is zeroed out
    net_ip = ip_int & subnet
    # heres where we do the iteration
    for x in range(count):
        #We start with the lowest address, the network address and add x each loop
        addr = net_ip + x
        #Construct an ip from the int we were working with previously, by seperating into octets and masking off what we don't need.
        range_out.append(f'{addr >> 24}.{(addr >> 16) & 0xFF}.{(addr >> 8) & 0xFF}.{addr & 0xFF}')
    return range_out



def main():
    scan()
if __name__ == "__main__":
    main()
