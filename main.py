# Author: BOB Marley (https://t.me/marleyybob123)
import requests
import os
import re
import time
import socket
import sys
from bs4 import BeautifulSoup
from pystyle import Write, Colors, Colorate, Center
from datetime import datetime

MAX_GRAB_LIMIT = 1_000_000

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    tld_grabber = r"""

████████╗██╗     ██████╗      ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
╚══██╔══╝██║     ██╔══██╗    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
   ██║   ██║     ██║  ██║    ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
   ██║   ██║     ██║  ██║    ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
   ██║   ███████╗██████╔╝    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
   ╚═╝   ╚══════╝╚═════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                
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
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, tld_grabber, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.yellow_to_green, by, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, bob_marley, 1)))
    print()
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    Write.Print(f"[!] Hostname: {host}\n", Colors.green_to_yellow, interval=0.002)
    Write.Print(f"[!] IP Address: {ip}\n\n", Colors.green_to_yellow, interval=0.002)

def get_domains(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', {'class': 'table-bordered'})
        if not table:
            return []
        return [re.sub(r'^\d+[:.\s]*', '', row.find_all('td')[0].text.strip())
                for row in table.find_all('tr')[1:]]
    except Exception as e:
        Write.Print(f"[!] Failed to fetch {url} - {e}\n", Colors.red, interval=0.001)
        return []

def save_to_file(domains, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a', encoding='utf-8') as f:
        for d in domains:
            f.write(d + '\n')

def scrape_tld(tld, limit):
    base_url = f"https://www.topsitessearch.com/domains/{tld}/"
    date_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join("Result", f"GRABBED_{tld}_{date_tag}.txt")
    total_grabbed = 0
    page = 1

    while total_grabbed < limit:
        url = f"{base_url}{page}/"
        Write.Print(f"[*] Grabbing page {page} for TLD: {tld}\n", Colors.purple_to_red, interval=0.001)
        domains = get_domains(url)

        if not domains:
            Write.Print("[!] No more domains found or failed to load.\n", Colors.red, interval=0.001)
            break

        to_save = domains[:limit - total_grabbed]
        save_to_file(to_save, output_file)
        total_grabbed += len(to_save)

        for d in to_save:
            Write.Print(f"[+] {d}\n", Colors.green_to_white, interval=0.0005)

        if total_grabbed >= limit:
            break

        page += 1
        time.sleep(1)

    Write.Print(f"\n[✓] Done! Grabbed {total_grabbed} domains. Saved to {output_file}\n", Colors.green_to_yellow, interval=0.002)

def main():
    banner()
    tld = Write.Input("Input Grabbing TLD (e.g., com, go.id): ", Colors.green_to_yellow, interval=0.005).strip()
    try:
        limit = int(Write.Input("How many domains to grab (max 1,000,000): ", Colors.green_to_yellow, interval=0.005).strip())
    except ValueError:
        Write.Print("[!] Invalid number.\n", Colors.red, interval=0.002)
        return

    if limit > MAX_GRAB_LIMIT:
        Write.Print(f"[!] Limit exceeds max allowed ({MAX_GRAB_LIMIT}). Aborting.\n", Colors.red, interval=0.002)
        return

    scrape_tld(tld, limit)

if __name__ == '__main__':
    main()
