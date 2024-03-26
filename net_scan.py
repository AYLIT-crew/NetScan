import scapy.all as scapy
from termcolor import colored as cl
from pyfiglet import figlet_format as ff
import subprocess, sys, requests, re, time, os

def check_if_root():
    if os.getuid() == 0:
        pass
    else:
        print(cl('You must be root in order to run this program', 'red'))
        sys.exit()

def scan_ports(prts, addr):
    ports = ",".join(prts)
    ctr = 'nmap '+f'-p{ports}'+f' {addr}'
    data = subprocess.check_output(ctr.split(' ')).decode().split('\n')
    ind = 0
    for i in range(len(data)):
        if 'PORT' in data[i]:
            ind = i
            break
    return data[ind:]

def getosversion(d):
    d = d.split('\n')
    ind = 0
    for i in range(len(d)):
        if 'Aggressive' in d[i]:
            ind = i
            break
    return d[ind]

def getversion(d):
    d = d.decode().split('\n')
    return d[0]

def get_ports_open(d):
    dsplit = d.split('\n')
    ind = 0
    for i in range(len(dsplit)):
        if 'PORT' in dsplit[i]:
            ind = i
    dsplit = dsplit[ind+1:-2]
    ports_open = []
    for i in dsplit:
        if 'open' in i or 'PORT' in i:
            ports_open.append(i)
    return ports_open

def get_ips(d):
    d = d.split('\n')
    for i in range(len(d)):
        if 'TRACEROUTE' in d[i]:
            ind = i
            break
    d = d[ind:]
    ips = []
    for i in d:
        search_result = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', i)
        if search_result != None:
            ips.append(search_result.group())
    return ips

def get_ip_info(d):
    url = 'http://ip-api.com'   
    infos = {}
    for i in d:
        req_url = url+'/'+'json/'+i
        req_data = requests.get(req_url).json()
        try:
            infos[i] = (req_data['isp'], req_data['city'], req_data['country'])
        except:
            pass
    return infos

def check_tool():
    output = subprocess.check_output(['nmap', '--version'])
    if 'Nmap' == output.decode().split('\n')[0].split()[0]:
        pass
    else:
        print(cl('Looks like Nmap is not installed in then system.', 'red'))
        opt = input(cl('Want to install Nmap(y/n)? ', 'yellow')).strip().lower()
        if opt == 'y':
            subprocess.call('sudo apt-get install nmap', shell=True)
            print('-'*10)
            print(cl('[+] Successfully installed.', 'green'))
            print('-'*20)
            subprocess.call('clear', shell=True)
        else:
            print(cl('Cannot run the program without Nmap, sorry.', 'red'))
            sys.exit()

check_if_root()
check_tool()

subprocess.call('clear', shell=True)

commands = {'getversion': 'To get the version of software run by the IP', 'getcommands': 'To get a list of commands which can be used for running a Nmap scan', 'trace': 'To trace the transfer of packets', 'getportsopen': 'To get a list of ports open in a host', 'getosversion': 'To predict the OS run by the IP',
            'stealthscan': 'Stealth Scan makes it difficult for the host to know about the scan', 'portsscan': 'To scan a list of ports of a host', 'hostdiscover': 'To discover hosts in a subnet',  'quit': 'To quit the program'}

while True:
    print(cl('='*40, 'red'))
    print(cl(ff('NetScan'), 'red'))
    print(cl('\t\t-Powered by Nmap\n\t\t-An AYLIT production\n\t\t-v1.0', 'red'))
    print(cl('='*40, 'red'), '\n')
    print(cl('Commands available:', 'red'))
    for i in commands:
        print(cl(f'   ->{i}({commands[i]})', 'red'))
    print('-'*20)
    cmd = input(cl('Enter the command:', 'yellow')).lower().strip()
    if cmd == 'quit':
        subprocess.call('clear', shell=True)
        sys.exit()
        print(cl(data.decode(), 'blue'))
    elif cmd == 'getcommands':
        data = subprocess.check_output(['nmap', '-h'])
        print('-'*20)
        print(cl(data.decode(), 'blue'))
    elif cmd == 'getversion':
        data = subprocess.check_output(['nmap', '--version'])
        print(cl(getversion(data), 'blue'))
        print('-'*20)
    elif cmd == 'hostdiscover':
        print('-'*10)
        print(cl("Fetching your router address using the 'route' command.", 'green'))
        print('-'*10)
        route_data = subprocess.check_output('route'.split()).decode().split('\n')
        router_ip = route_data[2].split()[1]
        ip_for_arp = ".".join(router_ip.split('.')[:-1])+'.0/24'
        arp_class = scapy.ARP(pdst=ip_for_arp)
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        broadcast_arp_request = broadcast/arp_class
        ans = scapy.srp(broadcast_arp_request, timeout=1, verbose=False)[0]
        ips = 0
        for i in ans:
            ips += 1
        print(cl(f'Hosts found: {str(ips)}', 'blue'))
        print(cl('    IP\t\t\t\tMAC', 'blue'))
        for i in ans:
            print(cl(i[1].psrc+'\t\t\t'+i[1].hwsrc, 'blue'))
        print('-'*20)
    else:
        addr = input(cl('Enter address:', 'yellow'))
        if cmd == 'trace':
            ctr = f'nmap --traceroute {addr}'
            print(cl(f'Command to run: {ctr}', 'red'))
            term_data = subprocess.check_output(ctr.split(' ')).decode()
            print('-'*10)
            print(cl('[+] Scan ran successfully', 'green'))
            print('-'*10)
            raw_opt = input(cl('See raw output(y/n)? ', 'red')).lower().strip()
            if raw_opt == 'y':
                print('-'*10)
                print(cl(term_data, 'blue'))
            else:
                ips = get_ips(term_data)
                ip_infos = get_ip_info(ips)
                print('-'*10)
                print(cl('Consolidated output:\n', 'red'))
                for i in ip_infos:
                    print('-'*10)
                    print(cl(f'IP:{i}', 'blue'))
                    print(cl(f'ISP:{ip_infos[i][0]}\nCity:{ip_infos[i][1]}\nCountry:{ip_infos[i][-1]}', 'blue'))
                    print('-'*10)
            print('-'*20)
        elif cmd == 'getportsopen':
            ctr = f'nmap {addr}'
            print(cl(f'Command to run: {ctr}', 'red'))
            term_data = subprocess.check_output(ctr.split(' ')).decode()
            print('-'*10)
            print(cl('[+] Scan ran successfully', 'green'))
            print('-'*10)
            get_open_ports = get_ports_open(term_data)
            print(cl('Ports open:\n'+'-'*10, 'blue'))
            if get_open_ports == []:
                print(cl(f'No ports open for {addr}', 'red'))
            else:
                for i in get_open_ports:
                    print(cl(i, 'blue'))
            print('-'*20)
        elif cmd == 'getosversion':
            ctr = f'nmap -O {addr}'
            print(cl(f'Command to run: {ctr}', 'red'))
            ags = input(cl('Aggressive OS guess(y/n)? ', 'yellow'))
            if ags == 'y':
                ctr = f'nmap -O --osscan-guess {addr}'
            data = subprocess.check_output(ctr.split(' ')).decode()
            print('-'*10)
            print(cl('[+] Scan ran successfully', 'green'))
            print('-'*10)
            get_os_data = getosversion(data)
            print(cl(get_os_data, 'blue'))
            print('-'*20)
        elif cmd == 'stealthscan':
            ctr = f'nmap -sS {addr}'
            print(cl(f'Command to run: {ctr}', 'red'))
            data = subprocess.check_output(ctr.split(' '))
            print('-'*10)
            print(cl('[+] Scan ran successfully', 'green'))
            print('-'*10)
            print(cl(data.decode(), 'blue'))
            print('-'*20)
        elif cmd == 'portsscan':
            ports_option = input(cl('Enter ports manually(y/n)? ', 'yellow'))
            if ports_option == 'y':
                ports = list(map(str, input(cl('Enter the ports(eg:- 22 35 45):', 'yellow')).split(' ')))
                print(cl("\n".join(scan_ports(ports, addr)), 'blue'))
            else:
                rnge = list(map(str, input(cl('Enter the starting range and ending range(eg:- 22 443)', 'yellow')).split(' ')))
                vals = []
                for i in range(int(rnge[0]), int(rnge[-1])+1):
                    vals.append(str(i))
                print(cl("\n".join(scan_ports(ports, addr)), 'blue'))
            print('-'*20)
        else:
            print(cl('Wrong option', 'red'))
            print('-'*20)
    press = input(cl('Press enter to clear screen', 'red'))
    if press == '':
        subprocess.call('clear', shell=True)
