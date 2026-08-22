import sys
from colorama import Fore, Style, init
from config.settings import PROJECT_ROOT
from scanners.github_scanner import run_github_scan
from core.database import db
from core.logger import setup_logger

init()

logger = setup_logger(__name__)

def print_banner():
    banner = f'''
{Fore.CYAN}
╔═══════════════════════════════════════════╗
║           FINSECURE v0.1.0                ║
║   Fintech API Key Exposure Detector       ║
╚═══════════════════════════════════════════╝
{Style.RESET_ALL}
    '''
    print(banner)

def show_menu():
    print(f"\n{Fore.YELLOW}=== Main Menu ==={Style.RESET_ALL}")
    print("1. Scan GitHub for exposed keys")
    print("2. Show all found keys")
    print("3. Exit")
    return input(f"\n{Fore.CYAN}Choose option (1-3): {Style.RESET_ALL}")

def show_found_keys():
    keys = db.get_all_keys()
    
    if not keys:
        print(f"{Fore.YELLOW}No keys found yet.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}=== Exposed Keys ==={Style.RESET_ALL}")
    print(f"Total found: {len(keys)}\n")
    
    for key in keys:
        key_id, key_value, key_type, source, source_url, found_at, risk, status, notes = key
        print(f"{Fore.RED}[CRITICAL]{Style.RESET_ALL} {key_value[:20]}...")
        print(f"  Type: {key_type}")
        print(f"  Source: {source}")
        print(f"  URL: {source_url}")
        print(f"  Found: {found_at}")
        print(f"  Status: {status}\n")

def main():
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            print(f"{Fore.CYAN}Starting GitHub scan...{Style.RESET_ALL}")
            run_github_scan()
        
        elif choice == '2':
            show_found_keys()
        
        elif choice == '3':
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}Invalid option. Try again.{Style.RESET_ALL}")

if __name__ == '__main__':
    main()
