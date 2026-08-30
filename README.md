# 🚀 Facebook Mass Reporter Bot

Automated tool to report multiple scam/fake Facebook accounts using Selenium WebDriver.

⚠️ **WARNING**: This tool can get your Facebook account banned. Use at your own risk.

---

## 📋 Features

- ✅ Automated login to Facebook
- ✅ Batch reporting of multiple accounts
- ✅ Customizable report reasons
- ✅ CAPTCHA prevention (auto-pause)
- ✅ Detailed logging & progress tracking
- ✅ Error handling & retry logic
- ✅ Report summary statistics

---

## 🛠️ Installation

### 1. Install Python 3.8+
```bash
python --version
```

### 2. Clone the repository
```bash
git clone https://github.com/kj-bot201/fb-mass-reporter-bot.git
cd fb-mass-reporter-bot
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download ChromeDriver
- Download from: https://chromedriver.chromium.org/
- Or use `webdriver-manager` (auto-installed)

---

## ⚙️ Configuration

### 1. Edit `config.json`
```json
{
  "email": "your_facebook_email@gmail.com",
  "password": "your_facebook_password",
  "accounts_file": "accounts.json",
  "headless": false
}
```

- **email**: Your Facebook account email
- **password**: Your Facebook password
- **accounts_file**: JSON file with accounts to report
- **headless**: Set to `true` to hide browser window

### 2. Edit `accounts.json`
```json
[
  {
    "url": "https://www.facebook.com/scam.account.1",
    "reason": "Fake Account"
  },
  {
    "url": "https://www.facebook.com/scam.account.2",
    "reason": "Scam/Fraud"
  }
]
```

**Supported Reasons:**
- `Fake Account`
- `Scam/Fraud`
- `Impersonation`
- `Spam`
- `Harassment`

---

## 🚀 Usage

### Run the reporter
```bash
python main.py
```

### Monitor progress
- Check `reporter.log` for detailed logs
- Console output shows real-time status

---

## 📊 Output

After running, you'll see:
```
=== REPORT SUMMARY ===
Successfully reported: 5
Failed: 1
Total: 6
```

All activity is logged in `reporter.log`

---

## ⚠️ Important Notes

1. **Account Ban Risk**: Facebook actively detects automation. Your account WILL likely be banned.

2. **CAPTCHA**: After 3-5 reports, you'll likely hit CAPTCHA. The tool pauses for 30 seconds.

3. **Delays**: The tool adds 5-second delays between reports to avoid detection.

4. **Valid URLs Only**: Make sure Facebook URLs are in correct format:
   - `https://www.facebook.com/username`
   - `https://www.facebook.com/123456789` (profile ID)

5. **Two-Factor Auth**: If you have 2FA enabled, you'll need to manually enter the code on first login.

---

## 🔧 Troubleshooting

### Issue: "WebDriver not found"
```bash
pip install webdriver-manager
```

### Issue: "Login failed"
- Check email/password in config.json
- Disable 2FA temporarily or enter code manually
- Check if Facebook is blocking your IP

### Issue: "Report button not found"
- Facebook UI changes frequently
- Update XPath selectors in `main.py`
- The tool may need adjustments

### Issue: "Stuck on CAPTCHA"
- The tool pauses automatically
- You may need to manually solve CAPTCHA
- Or increase pause time in code

---

## 📝 License

Educational use only. Users are responsible for their actions.

---

## ⚡ Disclaimer

This tool is provided **as-is** for educational purposes. The developer is NOT responsible for:
- Account bans
- Legal consequences
- Misuse of the tool
- Any damage caused

Use at your own risk.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Test thoroughly
2. Update XPath selectors if Facebook UI changes
3. Add error handling
4. Submit pull requests

---

## 📞 Support

For issues:
1. Check `reporter.log`
2. Review troubleshooting section
3. Test with single account first

---

**Last Updated:** August 2026
