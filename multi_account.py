#!/usr/bin/env python3

"""
Multi-Account Facebook Mass Reporter
Cycles through multiple accounts to avoid bans
"""

import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multi_reporter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MultiAccountReporter:
    def __init__(self, accounts_list, headless=False):
        """
        Initialize multi-account reporter
        accounts_list: List of dicts with email/password
        """
        self.accounts_list = accounts_list
        self.current_account_idx = 0
        self.headless = headless
        self.driver = None
        self.total_reported = 0
        self.total_failed = 0
        self.account_stats = {}
        
        # Initialize stats for each account
        for acc in accounts_list:
            email = acc.get('email')
            self.account_stats[email] = {'reported': 0, 'failed': 0, 'banned': False}
    
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
    
    def get_next_account(self):
        """Get next available account (skip banned ones)"""
        attempts = 0
        while attempts < len(self.accounts_list):
            account = self.accounts_list[self.current_account_idx]
            email = account.get('email')
            
            if not self.account_stats[email]['banned']:
                self.current_account_idx = (self.current_account_idx + 1) % len(self.accounts_list)
                return account
            
            logger.warning(f"⏭️  Skipping banned account: {email}")
            self.current_account_idx = (self.current_account_idx + 1) % len(self.accounts_list)
            attempts += 1
        
        logger.error("❌ All accounts are banned!")
        return None
    
    def login(self, email, password):
        """Login to Facebook with email/password"""
        try:
            logger.info(f"🔐 Attempting login as: {email}")
            self.driver.get('https://www.facebook.com/login')
            time.sleep(3)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.clear()
            email_field.send_keys(email)
            logger.info("✓ Email entered")
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "pass")
            password_field.clear()
            password_field.send_keys(password)
            logger.info("✓ Password entered")
            
            # Click login
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            
            time.sleep(5)
            
            # Check for CAPTCHA or login success
            current_url = self.driver.current_url
            
            if 'login' not in current_url and 'checkpoint' not in current_url:
                logger.info(f"✅ Login successful as {email}")
                return True
            elif 'checkpoint' in current_url:
                logger.warning(f"⚠️  2FA/Checkpoint required for {email}")
                logger.warning("Please complete 2FA in browser window...")
                time.sleep(60)  # Wait for manual 2FA
                return 'checkpoint' not in self.driver.current_url
            else:
                logger.error(f"❌ Login failed for {email}")
                self.account_stats[email]['banned'] = True
                return False
                
        except TimeoutException:
            logger.error(f"⏱️  Timeout during login for {email}")
            self.account_stats[email]['banned'] = True
            return False
        except Exception as e:
            logger.error(f"❌ Login error for {email}: {e}")
            self.account_stats[email]['banned'] = True
            return False
    
    def report_account(self, account_url, reason="Fake Account"):
        """Report a single Facebook account"""
        try:
            logger.info(f"📢 Reporting: {account_url}")
            
            self.driver.get(account_url)
            time.sleep(3)
            
            # Try to find and click menu button
            menu_xpaths = [
                \"//a[@aria-label='More']\",
                \"//div[@data-tooltip-content='More']\",
                \"//button[@aria-label='More']\",
                \"//a[contains(@aria-label, 'More')]\",
            ]
            
            menu_clicked = False
            for xpath in menu_xpaths:
                try:
                    menu_button = self.driver.find_element(By.XPATH, xpath)
                    menu_button.click()
                    menu_clicked = True
                    time.sleep(2)
                    break
                except:
                    continue
            
            if not menu_clicked:
                logger.warning(f"⚠️  Could not find menu for {account_url}")
                return False
            
            # Click report option
            report_xpaths = [
                \"//span[contains(text(), 'Report')]\",
                \"//div[contains(text(), 'Report')]\",
                \"//a[contains(text(), 'Report')]\",
                \"//li//a[contains(text(), 'Report')]\",
            ]
            
            report_clicked = False
            for xpath in report_xpaths:
                try:
                    report_button = self.driver.find_element(By.XPATH, xpath)
                    report_button.click()
                    report_clicked = True
                    time.sleep(2)
                    break
                except:
                    continue
            
            if not report_clicked:
                logger.warning(f"⚠️  Could not find report button")
                return False
            
            # Wait for dialog and select reason
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, \"//div[@role='dialog']\"))
                )
                time.sleep(1)
                
                # Click reason
                reason_xpaths = [
                    \"//span[contains(text(), 'Fake Account')]\",
                    \"//span[contains(text(), 'Scam')]\",
                    \"//span[contains(text(), 'Fraud')]\",
                    \"//span[contains(text(), 'Impersonation')]\",
                ]
                
                for xpath in reason_xpaths:
                    try:
                        reason_elem = self.driver.find_element(By.XPATH, xpath)
                        reason_elem.click()
                        time.sleep(1)
                        
                        # Click Next/Submit
                        submit_xpaths = [
                            \"//button[contains(text(), 'Next')]\",
                            \"//button[contains(text(), 'Submit')]\",
                            \"//button[contains(text(), 'Report')]\",
                        ]
                        
                        for submit_xpath in submit_xpaths:
                            try:
                                submit_btn = self.driver.find_element(By.XPATH, submit_xpath)
                                submit_btn.click()
                                time.sleep(2)
                                logger.info(f\"✅ Successfully reported: {account_url}\")
                                return True
                            except:
                                continue
                        break
                    except:
                        continue
            
            except TimeoutException:
                logger.warning(f\"⏱️  Timeout waiting for report dialog\")
        
        except Exception as e:
            logger.error(f\"❌ Error reporting {account_url}: {e}\")
        
        return False
    
    def report_multiple_accounts(self, targets_file, reports_per_account=5):
        \"\"\"
        Report multiple target accounts using multiple reporter accounts
        reports_per_account: How many reports before switching to next account
        \"\"\"
        try:
            with open(targets_file, 'r') as f:
                targets = json.load(f)
            
            logger.info(f\"\\n🚀 Starting mass report of {len(targets)} accounts\")
            logger.info(f\"📊 Using {len(self.accounts_list)} reporter accounts\")
            logger.info(f\"📝 {reports_per_account} reports per account before switching\\n\")
            
            report_count = 0
            current_reporter_account = None
            reports_with_current = 0
            
            for target_idx, target in enumerate(targets, 1):
                target_url = target.get('url')
                reason = target.get('reason', 'Fake Account')
                
                # Get next account after X reports
                if reports_with_current >= reports_per_account or current_reporter_account is None:
                    if current_reporter_account:
                        logger.info(f\"\\n⏭️  Switching to next account (limit reached)\\n\")
                    
                    current_reporter_account = self.get_next_account()
                    if not current_reporter_account:
                        logger.error(\"❌ No more accounts available!\")
                        break
                    
                    # Login with new account
                    email = current_reporter_account.get('email')
                    password = current_reporter_account.get('password')
                    
                    if not self.login(email, password):
                        logger.error(f\"❌ Failed to login with {email}, trying next...\")
                        self.account_stats[email]['banned'] = True
                        continue
                    
                    reports_with_current = 0
                
                email = current_reporter_account.get('email')
                
                logger.info(f\"\\n[{target_idx}/{len(targets)}] Using account: {email}\")
                logger.info(f\"Reports with this account: {reports_with_current + 1}/{reports_per_account}\")
                
                if self.report_account(target_url, reason):
                    self.account_stats[email]['reported'] += 1
                    self.total_reported += 1
                    reports_with_current += 1
                else:
                    self.account_stats[email]['failed'] += 1
                    self.total_failed += 1
                
                # Delay between reports
                time.sleep(5)
                
                # CAPTCHA prevention every 3 reports
                if self.total_reported % 3 == 0:
                    logger.warning(f\"⏸️  Pausing 30 seconds (CAPTCHA prevention)...\")
                    time.sleep(30)
            
            # Print summary
            self.print_summary()
            
        except FileNotFoundError:
            logger.error(f\"File not found: {targets_file}\")
        except json.JSONDecodeError:
            logger.error(f\"Invalid JSON in {targets_file}\")
        except Exception as e:
            logger.error(f\"Error: {e}\")
    
    def print_summary(self):
        \"\"\"Print detailed report summary\"\"\"
        logger.info(\"\\n\" + \"=\"*60)\n        logger.info(\"📊 MULTI-ACCOUNT REPORT SUMMARY\")\n        logger.info(\"=\"*60)\n        logger.info(f\"\\n✅ Total Successfully Reported: {self.total_reported}\")\n        logger.info(f\"❌ Total Failed: {self.total_failed}\")\n        logger.info(f\"📈 Success Rate: {self.total_reported/(self.total_reported+self.total_failed)*100:.1f}%\" if (self.total_reported+self.total_failed) > 0 else \"\")\n        \n        logger.info(f\"\\n📋 Per-Account Breakdown:\")\n        for email, stats in self.account_stats.items():\n            status = \"🚫 BANNED\" if stats['banned'] else \"✅ ACTIVE\"\n            logger.info(f\"  {email}: {stats['reported']} reported, {stats['failed']} failed {status}\")\n        \n        logger.info(\"\\n\" + \"=\"*60)\n    \n    def close(self):\n        \"\"\"Close WebDriver\"\"\"n        if self.driver:\n            self.driver.quit()\n            logger.info(\"Browser closed\")\n\ndef main():\n    # Load config\n    try:\n        with open('multi_config.json', 'r') as f:\n            config = json.load(f)\n    except FileNotFoundError:\n        logger.error(\"multi_config.json not found. Creating template...\")\n        template = {\n            \"accounts\": [\n                {\"email\": \"account1@gmail.com\", \"password\": \"password1\"},\n                {\"email\": \"account2@gmail.com\", \"password\": \"password2\"},\n                {\"email\": \"account3@gmail.com\", \"password\": \"password3\"}\n            ],\n            \"targets_file\": \"targets.json\",\n            \"reports_per_account\": 5,\n            \"headless\": False\n        }\n        with open('multi_config.json', 'w') as f:\n            json.dump(template, f, indent=2)\n        logger.error(\"Please edit multi_config.json and try again\")\n        return\n    \n    accounts = config.get('accounts', [])\n    targets_file = config.get('targets_file', 'targets.json')\n    reports_per_account = config.get('reports_per_account', 5)\n    headless = config.get('headless', False)\n    \n    if not accounts:\n        logger.error(\"No accounts in multi_config.json\")\n        return\n    \n    logger.info(f\"Loaded {len(accounts)} accounts\")\n    \n    # Create reporter and run\n    reporter = MultiAccountReporter(accounts, headless)\n    \n    try:\n        reporter.setup_driver()\n        reporter.report_multiple_accounts(targets_file, reports_per_account)\n    \n    finally:\n        reporter.close()\n\nif __name__ == \"__main__\":\n    main()\n