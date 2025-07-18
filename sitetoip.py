#!/usr/bin/env python3
import os
import requests
import sys
import time
from socket import gethostbyname
from concurrent.futures import ThreadPoolExecutor
from pystyle import Write, Colors, Colorate, Center
from colorama import init, Fore, Style

init(autoreset=True)

# Colorama shortcodes
r = Fore.RED + Style.BRIGHT
g = Fore.GREEN + Style.BRIGHT
c = Fore.CYAN + Style.BRIGHT
y = Fore.YELLOW + Style.BRIGHT
w = Fore.WHITE + Style.BRIGHT
o = Style.RESET_ALL

def banner():
    reverse_site_to_ip = r"""
    
███████╗██╗████████╗███████╗    ████████╗ ██████╗     ██╗██████╗ 
██╔════╝██║╚══██╔══╝██╔════╝    ╚══██╔══╝██╔═══██╗    ██║██╔══██╗
███████╗██║   ██║   █████╗         ██║   ██║   ██║    ██║██████╔╝
╚════██║██║   ██║   ██╔══╝         ██║   ██║   ██║    ██║██╔═══╝ 
███████║██║   ██║   ███████╗       ██║   ╚██████╔╝    ██║██║     
╚══════╝╚═╝   ╚═╝   ╚══════╝       ╚═╝    ╚═════╝     ╚═╝╚═╝     
                                                                                                
   """
    by = r"""
                                 
                        ██████╗ ██╗   ██╗
                        ██╔══██╗╚██╗ ██╔╝
                        ██████╔╝ ╚████╔╝ 
                        ██╔══██╗  ╚██╔╝  
                        ██████╔╝   ██║   
                        ╚═════╝    ╚═╝   
                 
    """
    bob_marley = r"""

██████╗  ██████╗ ██████╗     ███╗   ███╗ █████╗ ██████╗ ██╗     ███████╗██╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗    ████╗ ████║██╔══██╗██╔══██╗██║     ██╔════╝╚██╗ ██╔╝
██████╔╝██║   ██║██████╔╝    ██╔████╔██║███████║██████╔╝██║     █████╗   ╚████╔╝ 
██╔══██╗██║   ██║██╔══██╗    ██║╚██╔╝██║██╔══██║██╔══██╗██║     ██╔══╝    ╚██╔╝  
██████╔╝╚██████╔╝██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██║███████╗███████╗   ██║   
╚═════╝  ╚═════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   

[!] AUTHOR : Bob Marley [https://t.me/marleyybob123]
[!] Note: Domain list should NOT include http:// or slashes
                                                                                 
   """
    print()
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, reverse_site_to_ip, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.yellow_to_green, by, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, bob_marley, 1)))
    print()

def sitetoip(i):
    try:
        ip = gethostbyname(i)
        print(f"{g}[+] {y}{i}{o} == {g}[{ip}]")
        with open('ips.txt', 'a') as f:
            f.write(ip + '\n')
    except:
        print(f"{r}[-] {y}{i}{o} == {r}[ ERROR ]")

def Main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()

    try:
        lists = Write.Input("\n[?] Enter your domain list filename (e.g., sites.txt): ", Colors.green_to_blue, interval=0.002).strip()
        thread = Write.Input("[?] Enter number of threads (e.g., 5): ", Colors.green_to_blue, interval=0.002).strip()

        print()  # spacing
        with open(lists, 'r') as f:
            targets = [x.strip() for x in f.readlines() if x.strip()]

        with ThreadPoolExecutor(max_workers=int(thread)) as executor:
            for domain in targets:
                executor.submit(sitetoip, domain)

    except Exception as e:
        print(f"{r}[!] Error: {str(e)}{o}")

if __name__ == '__main__':
    Main()
