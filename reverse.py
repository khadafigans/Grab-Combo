# -*- coding: utf-8 -*-
#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from colorama import Fore, Style, init
import threading
from pystyle import Write, Colors, Colorate, Center
import socket
import time

init(autoreset=True)

# Console color shortcuts
LIME = Fore.LIGHTGREEN_EX
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
RESET = Style.RESET_ALL

write_lock = threading.Lock()
print_lock = threading.Lock()
results_path = None

def banner():
    reverse_ip_to_site = r"""
    
██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗    ██╗██████╗ 
██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝    ██║██╔══██╗
██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗      ██║██████╔╝
██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝      ██║██╔═══╝ 
██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗    ██║██║     
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝╚═╝     
                                                                                                
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
                                                                                 
   """
    print()
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, reverse_ip_to_site, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.yellow_to_green, by, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, bob_marley, 1)))
    print()
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    Write.Print(f"[!] Hostname: {host}\n", Colors.green_to_yellow, interval=0.002)
    Write.Print(f"[!] IP Address: {ip}\n", Colors.green_to_yellow, interval=0.002)
    Write.Print("[!] Create 'list.txt' with IPs (1 per line)\n", Colors.yellow_to_red, interval=0.002)
    Write.Print("[!] Tool grabs all domains from RapidDNS sameIP\n", Colors.yellow_to_red, interval=0.002)
    Write.Print("[!] Output: Results/Results_<timestamp>.txt\n\n", Colors.green_to_yellow, interval=0.002)

def scrape_rapiddns_all_pages(ip, max_retries=3):
    headers = {'User-Agent': 'Mozilla/5.0'}
    domains = set()
    page = 1

    while True:
        url = f"https://rapiddns.io/sameip/{ip}?page={page}#result"
        tries = 0

        while tries < max_retries:
            try:
                res = requests.get(url, headers=headers, timeout=20)
                if res.status_code != 200 or "captcha" in res.text.lower():
                    raise Exception("Blocked or failed to fetch.")
                break
            except Exception as e:
                tries += 1
                if tries >= max_retries:
                    with print_lock:
                        print(f"{Fore.RED}[ERROR] Page {page} failed for {ip}: {e}{RESET}")
                    return domains
                time.sleep(2)

        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find("table")
        if not table:
            break

        rows = table.find_all("tr")[1:]
        if not rows:
            break

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                domain = cols[0].text.strip()  # ✅ FIXED: correct column is first!
                if domain:
                    domains.add(domain)

        page += 1

    return domains

def process_ip(ip):
    if ':' in ip:
        with print_lock:
            print(f"{Fore.RED}[SKIPPED] IPv6 not supported: {ip}{RESET}")
        return set()

    domains = scrape_rapiddns_all_pages(ip)

    with print_lock:
        if domains:
            print(f"{LIME}+---------------------[Results Found]--------------------+{RESET}")
            print(f"{CYAN}[INFO]{RESET} IP: {WHITE}{ip}{RESET}")
            print(f"{LIME}✔ [SUCCESS]{RESET} {len(domains)} domain(s) found.")
            print(f"{LIME}+--------------------------------------------------------+{RESET}")
        else:
            print(f"{Fore.RED}+----------------------[Failed]--------------------------+{RESET}")
            print(f"{CYAN}[INFO]{RESET} IP: {WHITE}{ip}{RESET}")
            print(f"{Fore.RED}✖ [FAILED]{RESET} No domains found.")
            print(f"{Fore.RED}+--------------------------------------------------------+{RESET}")

    if domains:
        with write_lock:
            with open(results_path, "a", encoding="utf-8") as f:
                for d in sorted(domains):
                    f.write(d + "\n")

    return domains

def main():
    global results_path
    banner()
    try:
        list_file = Write.Input("[?] Enter your list file (e.g., list.txt): ", Colors.yellow_to_red, interval=0.002).strip()
        with open(list_file, 'r', encoding="utf-8") as f:
            ip_list = [line.strip() for line in f if line.strip()]

        os.makedirs("Results", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_path = os.path.join("Results", f"Results_{timestamp}.txt")
        open(results_path, "w").close()  # start fresh

        all_domains = set()
        for ip in ip_list:
            result = process_ip(ip)
            all_domains.update(result)

        print(f"\n{LIME}[INFO] Total unique domains found: {len(all_domains)}{RESET}")
        print(f"{CYAN}[INFO] Results saved to {results_path}{RESET}")

    except Exception as e:
        print(f"{Fore.RED}[ERROR] {e}{RESET}")

if __name__ == '__main__':
    main()
