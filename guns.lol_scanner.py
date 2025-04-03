import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style

init()
def check_username(username):
    """Check if a username is available on guns.lol"""
    username = username.strip()
    if not username:
        return None
    
    url = f"https://guns.lol/{username}"
    try:
        response = requests.get(url)

        if "This user is not claimed" in response.text:
            return (username, True)
        else:
            return (username, False)
    except Exception as e:
        print(f"{Fore.RED}Error checking {username}: {str(e)}{Style.RESET_ALL}")
        return (username, None)

def main():

    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usernames.txt")
    
    if not os.path.exists(input_file):
        print(f"{Fore.RED}File not found: {input_file}{Style.RESET_ALL}")
        return
    
    try:
        threads = int(input(f"{Fore.CYAN}Enter number of threads (1-10, default 5): {Style.RESET_ALL}") or "5")
        threads = max(1, min(10, threads))
    except ValueError:
        threads = 5
        print(f"{Fore.YELLOW}Invalid input, using 5 threads{Style.RESET_ALL}")
    

    with open(input_file, 'r', encoding='utf-8') as f:
        usernames = f.readlines()
    
    usernames = [u.strip() for u in usernames if u.strip()]
    total = len(usernames)
    
    print(f"{Fore.GREEN}Loaded {total} usernames to check from usernames.txt{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Starting scan with {threads} threads...{Style.RESET_ALL}")
    
    available_file = "available_usernames.txt"
    
    available_count = 0
    taken_count = 0
    

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(check_username, usernames))
    

    with open(available_file, 'w', encoding='utf-8') as avail_f:
        
        for username, is_available in results:
            if is_available is None:
                continue
                
            if is_available:
                avail_f.write(f"{username}\n")
                print(f"{Fore.GREEN}[AVAILABLE] {username}{Style.RESET_ALL}")
                available_count += 1
            else:
                print(f"{Fore.RED}[TAKEN] {username}{Style.RESET_ALL}")
                taken_count += 1
    
    print(f"\n{Fore.CYAN}Scan Complete!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Available usernames: {available_count}{Style.RESET_ALL}")
    print(f"{Fore.RED}Taken usernames: {taken_count}{Style.RESET_ALL}")
    print(f"Results saved to {available_file}")

if __name__ == "__main__":
    main()