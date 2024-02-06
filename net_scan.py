import time, re
import subprocess, sys, requests
from termcolor import colored as cl
from pyfiglet import figlet_format as ff

try:
    subprocess.call('cls', shell=True)
except:
    subprocess.call('clear', shell=True)

print(cl('='*40, 'red'))
print(cl(ff('NetScan'), 'red'))
print(cl('\t\t-Powered by Nmap\n\t\t-An AYLIT production\n\t\t-v1.0', 'red'))
print(cl('='*40, 'red'), '\n')

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
        if search_result  != None:
            ips.append(search_result.group())
    return ips

def get_ip_info(d):
    url = 'https://ipapi.co/'
    infos = {}
    for i in d:
        req_url = url+i+'/'+'json/'
        req_data = requests.get(req_url).json()
        try:
            infos[i] = [req_data['org'], req_data['city'], req_data['country']]
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
            print(cl('Successfully installed.', 'green'))
            print('-'*20)
        else:
            print(cl('Cannot run the program without Nmap, sorry.', 'red'))
            sys.exit()

check_tool()

print(cl('Commands available:\n   ->getversion(To get the version of software run by the IP)\n   ->getcommands(To get a list of commands which can be used for running a Nmap scan)\n   ->trace(To trace the transfer of packets)\n   ->quit(To quit the program)', 'red'))

print('-'*20)

while True:
    cmd = input(cl('Enter the command:', 'yellow')).lower().strip()
    if cmd == 'quit':
        sys.exit()
    elif cmd == 'getcommands':
        subprocess.call('nmap -h', shell=True)
        print('-'*20)
    else:
        pass
    addr = input(cl('Enter the IP or address of the webiste to run a nmap scan on:', 'yellow'))
    if cmd == 'getversion':
        ctr = f'nmap -sV {addr}'
        print(cl(f'Command to be run: {ctr}', 'red'))
        subprocess.call(ctr, shell=True)
        print('-'*20)
    elif cmd == 'trace':
        ctr = f'nmap --traceroute {addr}'
        print(cl(f'Command to be run: {ctr}', 'red'))
        term_data = subprocess.check_output(['nmap', '--traceroute', addr]).decode()
        ips = get_ips(term_data)
        ips_info = get_ip_info(ips)
        print('-'*10)
        raw_opt = input(cl('See raw output(y/n)? ', 'red')).lower().strip()
        if raw_opt == 'y':
            print(term_data)
        else:
            print('-'*10)
            print(cl('Consolidated output:\n', 'red'))
            for i in ips_info:
                print('-'*20)
                print(cl(f'Organisation:{ips_info[i][0]}\nCity:{ips_info[i][1]}\nCountry:{ips_info[i][-1]}', 'blue'))
                print('-'*10)
        print('-'*20)
