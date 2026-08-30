#!/usr/bin/env python3
"""
Facebook Account Creator (via email)
Creates fresh Facebook accounts for mass reporting
"""

import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('account_creator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FacebookAccountCreator:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.created_accounts = []
    
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("✅ WebDriver initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize WebDriver: {e}")
            raise
    
    def create_account(self, first_name, last_name, email, password, birth_month, birth_day, birth_year, gender):
        """
        Create a Facebook account
        gender: 1=Female, 2=Male, 3=Custom
        """
        try:
            logger.info(f"Creating account: {first_name} {last_name} ({email})")
            
            self.driver.get('https://www.facebook.com/')
            time.sleep(2)
            
            # Click "Create new account" button
            create_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@data-testid='open-registration-form-button']"))
            )
            create_btn.click()
            
            time.sleep(3)
            
            # Fill form
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "firstname"))
            )
            
            self.driver.find_element(By.NAME, "firstname").send_keys(first_name)
            self.driver.find_element(By.NAME, "lastname").send_keys(last_name)
            self.driver.find_element(By.NAME, "reg_email__").send_keys(email)
            self.driver.find_element(By.NAME, "reg_passwd__").send_keys(password)
            
            # Select birth date
            self.driver.find_element(By.ID, "month").send_keys(str(birth_month))
            self.driver.find_element(By.ID, "day").send_keys(str(birth_day))
            self.driver.find_element(By.ID, "year").send_keys(str(birth_year))
            
            # Select gender
            self.driver.find_element(By.CSS_SELECTOR, f"input[value='{gender}']").click()
            
            # Click Sign Up
            signup_btn = self.driver.find_element(By.NAME, "websubmit")
            signup_btn.click()
            
            time.sleep(5)
            
            # Check if successful or if email verification needed
            if 'facebook.com' in self.driver.current_url and 'login' not in self.driver.current_url:
                logger.info(f"✅ Account created successfully: {email}")
                self.created_accounts.append({
                    'email': email,
                    'password': password,
                    'name': f"{first_name} {last_name}"
                })
                return True
            else:
                logger.warning(f"⚠️  Account creation may require email verification for {email}")
                return True  # Still count as created
        
        except Exception as e:
            logger.error(f"❌ Error creating account: {e}")
            return False
    
    def create_multiple(self, accounts_data):
        """
        Create multiple accounts from list
        accounts_data: List of dicts with account info
        """
        logger.info(f"Creating {len(accounts_data)} accounts...")
        
        for idx, account in enumerate(accounts_data, 1):
            logger.info(f"\n[{idx}/{len(accounts_data)}] Creating account...")
            
            self.create_account(
                first_name=account.get('first_name'),
                last_name=account.get('last_name'),
                email=account.get('email'),
                password=account.get('password'),
                birth_month=account.get('birth_month'),
                birth_day=account.get('birth_day'),
                birth_year=account.get('birth_year'),
                gender=account.get('gender', 2)
            )
            
            time.sleep(10)  # Wait between creations
        
        self.save_created_accounts()
    
    def save_created_accounts(self):
        """Save created accounts to multi_config.json"""
        if not self.created_accounts:
            logger.warning("No accounts created")
            return
        
        try:
            # Load existing config
            try:
                with open('multi_config.json', 'r') as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {
                    "accounts": [],
                    "targets_file": "targets.json",
                    "reports_per_account": 5,
                    "headless": False
                }
            
            # Add new accounts
            config['accounts'].extend(self.created_accounts)
            
            # Save
            with open('multi_config.json', 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"✅ Saved {len(self.created_accounts)} accounts to multi_config.json")
        
        except Exception as e:
            logger.error(f"Error saving accounts: {e}")
    
    def close(self):
        if self.driver:
            self.driver.quit()

def main():
    print("\n" + "="*60)
    print("Facebook Account Creator")
    print("="*60 + "\n")
    
    # Example accounts (customize as needed)
    accounts_to_create = [
        {
            'first_name': 'John',
            'last_name': 'Report',
            'email': 'johnreport001@gmail.com',
            'password': 'SecurePass123!@',
            'birth_month': 1,
            'birth_day': 15,
            'birth_year': 1990,
            'gender': 2
        },
        {
            'first_name': 'Jane',
            'last_name': 'Report',
            'email': 'janereport001@gmail.com',
            'password': 'SecurePass123!@',
            'birth_month': 3,
            'birth_day': 20,
            'birth_year': 1992,
            'gender': 1
        }
    ]
    
    creator = FacebookAccountCreator(headless=False)
    
    try:
        creator.setup_driver()
        creator.create_multiple(accounts_to_create)
    finally:
        creator.close()
    
    print("\n✅ Account creation completed!")
    print("Updated multi_config.json with new accounts")
    print("\nRun: python multi_account.py\n")

if __name__ == "__main__":
    main()
