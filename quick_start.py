#!/usr/bin/env python3
"""
Quick Start Guide for Facebook Mass Reporter Bot
"""

import json
import os

def create_config():
    """Create config.json interactively"""
    print("\n" + "="*50)
    print("Facebook Mass Reporter - Quick Start Setup")
    print("="*50 + "\n")
    
    print("⚠️  WARNING: This tool will likely get your account banned!\n")
    
    email = input("Enter your Facebook email: ").strip()
    password = input("Enter your Facebook password: ").strip()
    headless = input("Run in headless mode? (y/n, default: n): ").strip().lower() == 'y'
    
    config = {
        "email": email,
        "password": password,
        "accounts_file": "accounts.json",
        "headless": headless
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ config.json created!")

def create_accounts():
    """Create accounts.json interactively"""
    print("\n" + "="*50)
    print("Add Facebook Accounts to Report")
    print("="*50 + "\n")
    
    accounts = []
    
    print("Enter Facebook profile URLs (one per line)")
    print("Format: https://www.facebook.com/username or https://www.facebook.com/12345")
    print("Leave blank to finish\n")
    
    while True:
        url = input(f"Account #{len(accounts)+1} URL (or press Enter to finish): ").strip()
        if not url:
            break
        
        reason = input("  Reason (Fake Account/Scam/Impersonation/Spam) [Fake Account]: ").strip()
        if not reason:
            reason = "Fake Account"
        
        accounts.append({
            "url": url,
            "reason": reason
        })
        print()
    
    if accounts:
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=2)
        
        print(f"\n✅ {len(accounts)} account(s) added to accounts.json")
    else:
        print("\n❌ No accounts added!")

def main():
    print("\n" + "#"*50)
    print("# Facebook Mass Reporter Bot - Quick Start")
    print("#"*50)
    
    # Check for config
    if not os.path.exists('config.json'):
        print("\n📝 config.json not found. Let's create it...")
        create_config()
    else:
        print("\n✅ config.json found")
    
    # Check for accounts
    if not os.path.exists('accounts.json'):
        print("\n📝 accounts.json not found. Let's create it...")
        create_accounts()
    else:
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)
        print(f"\n✅ accounts.json found with {len(accounts)} account(s)")
    
    print("\n" + "="*50)
    print("Ready to start? Run: python main.py")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
