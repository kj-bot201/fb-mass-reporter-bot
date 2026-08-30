#!/usr/bin/env python3

"""
Fully Automated Facebook Account Creator
Creates multiple accounts automatically with random data
"""

import time
import json
import logging
import random
import string
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

class AutoAccountCreator:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.created_accounts = []
        self.first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emma", "Robert", "Lisa", "James", "Mary"]
        self.last_names = ["Report", "User", "Test", "Admin", "Check", "Verify", "Review", "Monitor", "Control", "Track"]
    
    def setup_driver(self):
        """Initialize Selenium WebDriver"""
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
    
    def generate_random_email(self, email_domain="gmail.com"):
        """Generate random email address"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"fbreport{random_string}@{email_domain}"
    
    def generate_password(self, length=12):
        """Generate secure random password"""
        characters = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choices(characters, k=length))
    
    def generate_name(self):
        """Generate random name"""
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        return first, last
    
    def generate_birthdate(self):
        """Generate random birth date (18+ years old)"""
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        year = random.randint(1990, 2005)  # Ensures 18+ years old
        return month, day, year
    
    def generate_gender(self):
        """Generate random gender"""
        return random.choice([1, 2, 3])  # 1=Female, 2=Male, 3=Custom
    
    def create_account(self, first_name, last_name, email, password, birth_month, birth_day, birth_year, gender):
        """Create a Facebook account"""
        try:
            logger.info(f"🔄 Creating: {first_name} {last_name} ({email})")
            
            self.driver.get('https://www.facebook.com/')
            time.sleep(3)
            
            # Click "Create new account" button
            try:
                create_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='open-registration-form-button']"))
                )
                create_btn.click()
                logger.info("  ✓ Form opened")
            except:
                logger.warning("  ⚠️  Could not find create account button")
                return False
            
            time.sleep(3)
            
            # Wait for form to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "firstname"))
                )
            except:
                logger.warning("  ⚠️  Form did not load properly")
                return False
            
            # Fill first name
            first_name_field = self.driver.find_element(By.NAME, "firstname")
            first_name_field.clear()
            first_name_field.send_keys(first_name)
            logger.info("  ✓ First name entered")
            
            # Fill last name
            last_name_field = self.driver.find_element(By.NAME, "lastname")
            last_name_field.clear()
            last_name_field.send_keys(last_name)
            logger.info("  ✓ Last name entered")
            
            # Fill email
            email_field = self.driver.find_element(By.NAME, "reg_email__")
            email_field.clear()
            email_field.send_keys(email)
            logger.info("  ✓ Email entered")
            
            # Fill password
            password_field = self.driver.find_element(By.NAME, "reg_passwd__")
            password_field.clear()
            password_field.send_keys(password)
            logger.info("  ✓ Password entered")
            
            time.sleep(2)
            
            # Select birth month
            try:
                month_field = self.driver.find_element(By.ID, "month")
                month_field.send_keys(str(birth_month))
                logger.info("  ✓ Birth month selected")
            except Exception as e:
                logger.warning(f"  ⚠️  Could not select month: {e}")
            
            # Select birth day
            try:
                day_field = self.driver.find_element(By.ID, "day")
                day_field.send_keys(str(birth_day))
                logger.info("  ✓ Birth day selected")
            except:
                pass
            
            # Select birth year
            try:
                year_field = self.driver.find_element(By.ID, "year")
                year_field.send_keys(str(birth_year))
                logger.info("  ✓ Birth year selected")
            except:
                pass
            
            time.sleep(2)
            
            # Select gender
            try:
                gender_options = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name='sex']")
                if gender < len(gender_options):
                    gender_options[gender-1].click()
                    logger.info("  ✓ Gender selected")
            except Exception as e:
                logger.warning(f"  ⚠️  Could not select gender: {e}")
            
            time.sleep(2)
            
            # Click Sign Up button
            try:
                signup_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "websubmit"))
                )
                signup_btn.click()
                logger.info("  ✓ Sign up clicked")
            except Exception as e:
                logger.warning(f"  ⚠️  Could not click signup: {e}")
                return False
            
            time.sleep(5)
            
            current_url = self.driver.current_url
            
            # Check if creation was successful
            if 'login' not in current_url.lower():
                logger.info(f"✅ Account created: {email}")
                self.created_accounts.append({
                    'email': email,
                    'password': password,
                    'name': f"{first_name} {last_name}"
                })
                return True
            else:
                logger.warning(f"⚠️  Account may need verification: {email}")
                self.created_accounts.append({
                    'email': email,
                    'password': password,
                    'name': f"{first_name} {last_name}",
                    'status': 'needs_verification'
                })
                return True
        
        except Exception as e:
            logger.error(f"❌ Error creating account: {e}")
            return False
    
    def create_accounts_batch(self, num_accounts=5, email_domain="gmail.com"):
        """Automatically create multiple accounts"""
        logger.info(f"\n🚀 Starting batch creation of {num_accounts} accounts\n")
        
        success_count = 0
        failed_count = 0
        
        for idx in range(1, num_accounts + 1):
            logger.info(f"\n[{idx}/{num_accounts}] ━━━━━━━━━━━━━━━━━━━━━━")
            
            try:
                # Generate random data
                first_name, last_name = self.generate_name()
                email = self.generate_random_email(email_domain)
                password = self.generate_password()
                birth_month, birth_day, birth_year = self.generate_birthdate()
                gender = self.generate_gender()
                
                # Create account
                if self.create_account(first_name, last_name, email, password, birth_month, birth_day, birth_year, gender):
                    success_count += 1
                else:
                    failed_count += 1
                
                # Wait between accounts
                if idx < num_accounts:
                    wait_time = random.randint(10, 20)
                    logger.info(f"⏸️  Waiting {wait_time}s before next account...")
                    time.sleep(wait_time)
            
            except Exception as e:
                logger.error(f"Error in batch creation: {e}")
                failed_count += 1
        
        # Print summary and save
        self.print_summary(success_count, failed_count)
        self.save_created_accounts()
    
    def print_summary(self, success, failed):
        """Print creation summary"""
        logger.info("\n" + "="*60)
        logger.info("📊 ACCOUNT CREATION SUMMARY")
        logger.info("="*60)
        logger.info(f"✅ Successfully created: {success}")
        logger.info(f"❌ Failed: {failed}")
        logger.info(f"📈 Total: {success + failed}")
        
        if success > 0:
            logger.info(f"\n📝 Created Accounts:")
            for idx, acc in enumerate(self.created_accounts, 1):
                status = f" (needs verification)" if acc.get('status') == 'needs_verification' else ""
                logger.info(f"  {idx}. {acc['email']}{status}")
        
        logger.info("="*60 + "\n")
    
    def save_created_accounts(self):
        """Save created accounts to multi_config.json"""
        if not self.created_accounts:
            logger.warning("No accounts created to save")
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
            logger.info(f"📁 Ready to use with: python multi_account.py\n")
        
        except Exception as e:
            logger.error(f"Error saving accounts: {e}")
    
    def close(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    print("\n" + "="*60)
    print("🤖 AUTOMATED FACEBOOK ACCOUNT CREATOR")
    print("="*60)
    print("\nThis tool will automatically create multiple Facebook accounts")
    print("and add them to multi_config.json for mass reporting.\n")
    
    try:
        num_accounts = int(input("How many accounts to create? (default: 5): ") or 5)
        email_domain = input("Email domain to use? (default: gmail.com): ") or "gmail.com"
        headless = input("Run in headless mode? (y/n, default: n): ").lower() == 'y'
        
        print(f"\n⚙️  Configuration:")
        print(f"  - Accounts to create: {num_accounts}")
        print(f"  - Email domain: {email_domain}")
        print(f"  - Headless mode: {headless}")
        print(f"\n⏳ This will take approximately {num_accounts * 20 // 60} minutes...\n")
        
        confirm = input("Continue? (y/n): ").lower()
        if confirm != 'y':
            print("Cancelled.")
            return
    
    except Exception as e:
        logger.error(f"Input error: {e}")
        num_accounts = 5
        email_domain = "gmail.com"
        headless = False
    
    creator = AutoAccountCreator(headless=headless)
    
    try:
        creator.setup_driver()
        creator.create_accounts_batch(num_accounts, email_domain)
    
    except KeyboardInterrupt:
        logger.warning("\n⛔ Process interrupted by user")
        creator.save_created_accounts()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        creator.save_created_accounts()
    
    finally:
        creator.close()
    
    print("\n✅ Account creation completed!")
    print("📝 Check 'account_creator.log' for details")
    print("🚀 Run: python multi_account.py\n")

if __name__ == "__main__":
    main()
