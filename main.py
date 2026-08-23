import sys
from colorama import Fore, Style, init
from config.settings import PROJECT_ROOT
from scanners.github_scanner import run_github_scan
from forensics.stripe_analyzer import analyze_exposed_key
from playbooks.stripe_remediation import remediate_stripe_key
from core.database import db
from core.logger import setup_logger

init()

logger = setup_logger(__name__)

def print_banner():
    banner = f'''
{Fore.CYAN}
╔═══════════════════════════════════════════╗
║           FINSECURE v0.3.0                ║
║   Fintech API Key Exposure Detector       ║
╚═══════════════════════════════════════════╝
{Style.RESET_ALL}
    '''
    print(banner)

def show_menu():
    print(f"\n{Fore.YELLOW}=== Main Menu ==={Style.RESET_ALL}")
    print("1. Scan GitHub for exposed keys")
    print("2. Show all found keys")
    print("3. Analyze key for fraud (forensics)")
    print("4. Remediate exposed key (auto-fix)")
    print("5. Exit")
    return input(f"\n{Fore.CYAN}Choose option (1-5): {Style.RESET_ALL}")

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

def analyze_key_interactive():
    key = input(f"{Fore.CYAN}Enter Stripe API key to analyze: {Style.RESET_ALL}")
    
    if not key.startswith('sk_'):
        print(f"{Fore.RED}Invalid key format (must start with sk_){Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}Analyzing key...{Style.RESET_ALL}")
    result = analyze_exposed_key(key, exposure_hours=24)
    
    if result is None:
        print(f"{Fore.RED}Analysis failed - invalid key or API error{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}=== Forensic Analysis ==={Style.RESET_ALL}")
    print(f"Exposure Window: {result['exposure_window_hours']} hours")
    print(f"Charges: {result['charges_count']}")
    print(f"Refunds: {result['refunds_count']}")
    print(f"Total Fraud: ${result['total_fraud_amount']:.2f}")
    print(f"Risk Level: {'CRITICAL' if result['high_risk'] else 'NORMAL'}")
    
    if result['fraud_alerts']:
        print(f"\n{Fore.RED}Fraud Alerts:{Style.RESET_ALL}")
        for alert in result['fraud_alerts']:
            print(f"  [{alert['severity']}] {alert['description']}")
    else:
        print(f"\n{Fore.GREEN}No fraud detected{Style.RESET_ALL}")

def remediate_key_interactive():
    key = input(f"{Fore.CYAN}Enter Stripe API key to remediate: {Style.RESET_ALL}")
    
    if not key.startswith('sk_'):
        print(f"{Fore.RED}Invalid key format{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}Starting automated remediation...{Style.RESET_ALL}\n")
    result = remediate_stripe_key(key)
    
    print(f"{Fore.YELLOW}=== Remediation Results ==={Style.RESET_ALL}")
    print(f"Playbook: {result['playbook']}")
    print(f"Status: {Fore.GREEN if result['overall_status'] == 'SUCCESS' else Fore.RED}{result['overall_status']}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Steps Executed:{Style.RESET_ALL}")
    for step in result['steps']:
        status_color = Fore.GREEN if step['status'] == 'SUCCESS' else Fore.RED
        print(f"  {status_color}[{step['status']}]{Style.RESET_ALL} {step['step']}")
        if 'message' in step:
            print(f"    → {step['message']}")

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
            analyze_key_interactive()
        
        elif choice == '4':
            remediate_key_interactive()
        
        elif choice == '5':
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}Invalid option. Try again.{Style.RESET_ALL}")

if __name__ == '__main__':
    main()