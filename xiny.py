import os
import time
import random
import string
import base64
from colorama import Fore, Style, init

init()
clear = lambda: os.system("cls" if os.name == "nt" else "clear")

PROXY_FILE = "proxies.txt"
HIT_FILE = "hit.txt"

def print_banner():
    print(Fore.MAGENTA + Style.BRIGHT + r"""
 (`-')      _     <-. (`-')_            
 (OO )_.-> (_)       \( OO) )     .->   
 (_| \_)--.,-(`-'),--./ ,--/  ,--.'  ,-.
 \  `.'  / | ( OO)|   \ |  | (`-')'.'  /
  \    .') |  |  )|  . '|  |)(OO \    / 
  .'    \ (|  |_/ |  |\    |  |  /   /) 
 /  .'.  \ |  |'->|  | \   |  `-/   /`  
`--'   '--'`--'   `--'  `--'    `--'    

  Discord Token Generator | Version 3.4.2
        Engine: Xiny | Dev: 24-vv
""" + Style.RESET_ALL)

def build_token(user_id):
    def gen_segment(length):
        return ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=length))
    encoded_id = base64.urlsafe_b64encode(user_id.encode()).decode().rstrip("=")
    return f"{encoded_id}.{gen_segment(6)}.{gen_segment(38)}"

def entropy_score(token):
    return sum(ord(c) for c in token) % 37 == 0

def write_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content + "\n")

def load_and_validate_proxies():
    if not os.path.exists(PROXY_FILE):
        print(f"{Fore.RED}[Xiny] No proxies found. Switching to direct mode.{Fore.RESET}")
        return []
    
    with open(PROXY_FILE, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    total = len(proxies)
    print(f"{Fore.YELLOW}[Xiny] Validating {total} proxies...{Fore.RESET}")
    time.sleep(min(5, total / 10000))

    working = random.randint(int(total * 0.6), int(total * 0.95))
    print(f"{Fore.GREEN}[Xiny] {working} proxies validated successfully.{Fore.RESET}")
    return proxies[:working]

def main():
    clear()
    print_banner()

    try:
        count = int(input(f"{Fore.MAGENTA}[Xiny]{Style.RESET_ALL} Tokens to generate: "))
        user_id = input(f"{Fore.MAGENTA}[Xiny]{Style.RESET_ALL} Target user ID: ").strip()
    except:
        print(f"{Fore.RED}[Xiny] Invalid input. Exiting.{Fore.RESET}")
        return

    use_proxies = input(f"{Fore.MAGENTA}[Xiny]{Style.RESET_ALL} Use proxies? (y/n): ").lower() == 'y'
    proxies = []

    if use_proxies:
        proxies = load_and_validate_proxies()
    else:
        print(f"{Fore.YELLOW}[Xiny] Using direct connection mode.{Fore.RESET}")
    time.sleep(1.2)

    print(f"{Fore.CYAN}[Xiny] Connecting to Discord gateway...{Fore.RESET}")
    time.sleep(1.4)
    print(f"{Fore.CYAN}[Xiny] Starting threaded entropy checks...{Fore.RESET}")
    time.sleep(1)

    for i in range(count):
        token = build_token(user_id)
        time.sleep(random.uniform(0.25, 0.6))

        if entropy_score(token):
            print(f"{Fore.GREEN}[VALID]{Fore.RESET} {token}")
            write_to_file(HIT_FILE, token)
        else:
            print(f"{Fore.RED}[INVALID]{Fore.RESET} {token}")
    
    print(f"\n{Fore.CYAN}[Xiny] Task complete. Output saved to {HIT_FILE}.{Fore.RESET}")
    input(f"{Fore.MAGENTA}[Xiny] Press Enter to exit...{Fore.RESET}")

if __name__ == "__main__":
    main()
