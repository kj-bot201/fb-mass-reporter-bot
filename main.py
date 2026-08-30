#!/usr/bin/env python3
"""
Facebook Mass Reporter Bot
Automated tool to report multiple Facebook accounts
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
        logging.FileHandler('reporter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FacebookReporter:
    def __init__(self, email, password, headless=False):
        self.email = email
        self.password = password
        self.driver = None
        self.headless = headless
        self.reported_count = 0
        self.failed_count = 0
        
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
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def login(self):
        """Login to Facebook"""
        try:
            logger.info("Attempting to login to Facebook...")
            self.driver.get('https://www.facebook.com/login')
            time.sleep(3)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(self.email)
            logger.info("Email entered")
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "pass")
            password_field.send_keys(self.password)
            logger.info("Password entered")
            
            # Click login button
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            
            time.sleep(5)
            
            # Check if login was successful
            if 'login' not in self.driver.current_url:
                logger.info("Login successful")
                return True
            else:
                logger.error("Login failed - still on login page")
                return False
                
        except TimeoutException:
            logger.error("Timeout during login")
            return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def report_account(self, account_url, reason="Fake Account"):
        """Report a single Facebook account"""
        try:
            logger.info(f"Attempting to report: {account_url}")
            
            # Navigate to account
            self.driver.get(account_url)
            time.sleep(3)
            
            # Click the menu button (three dots)
            menu_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@aria-label='More']|//div[@data-tooltip-content='More']"))
            )
            menu_button.click()
            time.sleep(2)
            
            # Click "Report this person" or "Report Account"
            report_options = [
                "//span[contains(text(), 'Report')]",
                "//div[contains(text(), 'Report')]",
                "//a[contains(text(), 'Report')]"
            ]
            
            report_clicked = False
            for xpath in report_options:
                try:
                    report_button = self.driver.find_element(By.XPATH, xpath)
                    report_button.click()
                    report_clicked = True
                    time.sleep(2)
                    break
                except:
                    continue
            
            if not report_clicked:
                logger.warning(f"Could not find report button for {account_url}")
                self.failed_count += 1
                return False
            
            # Select reason
            try:
                # Wait for dialog to appear
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                time.sleep(1)
                
                # Click on reason option (Fake Account, Spam, etc)
                reason_options = [
                    "//span[contains(text(), 'Fake Account')]",
                    "//span[contains(text(), 'Scam')]",
                    "//span[contains(text(), 'Fraud')]"
                ]
                
                reason_selected = False
                for xpath in reason_options:
                    try:
                        reason_elem = self.driver.find_element(By.XPATH, xpath)
                        reason_elem.click()
                        reason_selected = True
                        time.sleep(1)
                        break
                    except:
                        continue
                
                if reason_selected:
                    # Click Next/Submit button
                    submit_buttons = [
                        "//button[contains(text(), 'Next')]",
                        "//button[contains(text(), 'Submit')]",
                        "//button[contains(text(), 'Report')]"
                    ]
                    
                    for xpath in submit_buttons:
                        try:
                            submit_btn = self.driver.find_element(By.XPATH, xpath)
                            submit_btn.click()
                            time.sleep(2)
                            logger.info(f"✅ Successfully reported: {account_url}")
                            self.reported_count += 1
                            return True
                        except:
                            continue
            except TimeoutException:
                logger.warning(f"Timeout waiting for report dialog for {account_url}")
            
        except Exception as e:
            logger.error(f"Error reporting {account_url}: {e}")
            self.failed_count += 1
            return False
        
        return False
    
    def report_multiple(self, accounts_file):
        """Report multiple accounts from a file"""
        try:
            with open(accounts_file, 'r') as f:
                accounts = json.load(f)
            
            logger.info(f"Starting mass report process for {len(accounts)} accounts")
            
            for idx, account in enumerate(accounts, 1):
                logger.info(f"\n[{idx}/{len(accounts)}] Processing account...")
                
                url = account.get('url')
                reason = account.get('reason', 'Fake Account')
                
                if url:
                    self.report_account(url, reason)
                    time.sleep(5)  # Wait between reports
                
                # CAPTCHA check every 3 reports
                if idx % 3 == 0:
                    logger.warning("⚠️  Pausing for 30 seconds (CAPTCHA prevention)")
                    time.sleep(30)
            
            logger.info(f"\n\n=== REPORT SUMMARY ===")
            logger.info(f"Successfully reported: {self.reported_count}")
            logger.info(f"Failed: {self.failed_count}")
            logger.info(f"Total: {len(accounts)}")
            
        except FileNotFoundError:
            logger.error(f"File not found: {accounts_file}")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {accounts_file}")
        except Exception as e:
            logger.error(f"Error in report_multiple: {e}")
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")

def main():
    # Load configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error("config.json not found. Please create it first.")
        return
    
    email = config.get('email')
    password = config.get('password')
    accounts_file = config.get('accounts_file', 'accounts.json')
    headless = config.get('headless', False)
    
    if not email or not password:
        logger.error("Email and password must be provided in config.json")
        return
    
    # Create reporter and run
    reporter = FacebookReporter(email, password, headless)
    
    try:
        reporter.setup_driver()
        
        if reporter.login():
            reporter.report_multiple(accounts_file)
        else:
            logger.error("Failed to login. Exiting.")
    
    finally:
        reporter.close()

if __name__ == "__main__":
    main()
