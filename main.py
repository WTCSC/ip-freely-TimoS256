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


def scan(ip):
    print(ip)
    ips = getrange(ip)
    out = []
    h = 0
    for x in ips:
        h += 1
        print(x)
        print(h)
        result = ping(x)
        print(result)
        host = lookup(x)
        print(host)
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
def lookup(ip):
    try:
        return socket.gethostbyaddr(ip)
    except:
        return "Failed"

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
