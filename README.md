# LinkedIn API Scraper

A Python script for scraping LinkedIn posts using their GraphQL API with anti-detection measures.

## ⚠️ Important Security Notice

This project requires LinkedIn authentication tokens that are **personal and sensitive**. Never share your tokens publicly!

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd linkedin-api-project
```

### 2. Install Dependencies
```bash
pip install requests
```

### 3. Configure Authentication (REQUIRED)
```bash
# Copy the template config file
cp config_template.py config.py

# Edit config.py with your LinkedIn authentication tokens
# See linkedin_auth_guide.md for detailed instructions
```

### 4. Get Your LinkedIn Tokens
Follow the detailed guide in `linkedin_auth_guide.md` to extract your LinkedIn authentication tokens using browser developer tools.

### 5. Run the Scraper
```bash
python linkedin_api_call.py
```

## 📁 Project Structure

- `linkedin_api_call.py` - Main scraper script
- `config_template.py` - Template for authentication config (safe to share)
- `config.py` - Your actual tokens (DO NOT share, auto-ignored by git)
- `linkedin_auth_guide.md` - Detailed guide for getting LinkedIn tokens
- `.gitignore` - Prevents sensitive files from being committed

## 🔧 Configuration

Edit the search settings in `linkedin_api_call.py`:

```python
SEARCH_KEYWORDS = "hiring marketing dubai"  # What to search for
TARGET_POSTS = 40                          # Number of posts to scrape
POSTS_PER_PAGE = 10                        # Posts per page
BASE_DELAY = 2                             # Delay between requests
```

## 🛡️ Security Features

- **Token separation**: Sensitive tokens are kept in a separate config file
- **Git ignore**: Sensitive files are automatically excluded from version control
- **Rate limiting**: Built-in delays to avoid being blocked
- **User agent rotation**: Anti-detection measures

## 📊 Output

The scraper generates:
- CSV file with post data
- JSON backup file with raw data
- Detailed logs

## ⚠️ Important Notes

1. **Use responsibly**: Respect LinkedIn's terms of service
2. **Rate limiting**: Don't scrape too aggressively
3. **Token updates**: Tokens expire and need periodic updates
4. **Account safety**: Consider using a dedicated account for scraping

## 🔍 Troubleshooting

- **403 Forbidden errors**: Your tokens have expired, update them
- **No results**: Check your search keywords or page instance
- **Rate limited**: Increase delays in configuration

## 📖 Documentation

See `linkedin_auth_guide.md` for detailed instructions on:
- Getting authentication tokens
- Updating expired tokens
- Troubleshooting common issues

## 🚨 Security Reminder

**NEVER commit your `config.py` file or share your LinkedIn tokens publicly!** 