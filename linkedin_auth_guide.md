# LinkedIn Authentication Guide

## 🔐 How to Update Authentication Tokens

When your LinkedIn tokens expire (you'll get 403 errors), follow these steps to get fresh authentication data:

### Method 1: Using Browser Developer Tools (Recommended)

#### Step 1: Open LinkedIn in Browser
1. Open Chrome/Edge and go to https://www.linkedin.com
2. Log in to your LinkedIn account
3. Press `F12` to open Developer Tools
4. Go to the **Network** tab

#### Step 2: Perform a Search
1. In LinkedIn, search for something like "hiring marketing dubai"
2. In Developer Tools, look for requests to `voyager/api/graphql`
3. Click on one of these GraphQL requests

#### Step 3: Extract Authentication Data
In the request details, look for:

**Headers Tab:**
```
csrf-token: ajax:1234567890123456789
x-li-page-instance: urn:li:page:p_flagship3_search_srp_content;XXXXXX
```

**Cookies (in Request Headers):**
```
Cookie: JSESSIONID=ajax:1234567890123456789; li_at=AQXXXXXXXXXXXX; li_rm=AQXXXXXXXXXXXX; bcookie=vXXXXXXX; bscookie=vXXXXXXX; lidc=bXXXXXXX
```

#### Step 4: Update Configuration
Copy these values to your `linkedin_api_call.py` configuration section:

```python
# Main authentication tokens
CSRF_TOKEN = "ajax:1234567890123456789"  # From csrf-token header
JSESSIONID = "ajax:1234567890123456789"  # From JSESSIONID cookie

# LinkedIn authentication cookies
LI_AT_TOKEN = "AQXXXXXXXXXXXX"  # From li_at cookie
LI_RM_TOKEN = "AQXXXXXXXXXXXX"  # From li_rm cookie

# Browser/device cookies
BCOOKIE = "vXXXXXXX"      # From bcookie
BSCOOKIE = "vXXXXXXX"     # From bscookie
LIDC_COOKIE = "bXXXXXXX"  # From lidc cookie

# Page instance
PAGE_INSTANCE = "urn:li:page:p_flagship3_search_srp_content;XXXXXX"
```

### Method 2: Using Curl Command (Advanced)

If you have a working curl command from LinkedIn mobile/web:

1. Extract the tokens from the curl headers
2. Update the configuration variables accordingly

### Method 3: Using Frida/Proxy (Expert Level)

If you have SSL bypass working:
1. Capture the LinkedIn API calls
2. Extract the authentication headers
3. Update the tokens

## 🔍 Token Types Explained

| Token | Purpose | Frequency of Change |
|-------|---------|-------------------|
| **csrf-token** | CSRF protection | Changes with each session |
| **JSESSIONID** | Session identifier | Changes with each session |
| **li_at** | LinkedIn authentication | Changes periodically (days/weeks) |
| **li_rm** | Remember me token | Changes less frequently |
| **bcookie** | Browser identification | Rarely changes |
| **bscookie** | Browser session | Changes with sessions |
| **lidc** | Load balancer routing | Changes occasionally |

## ⚠️ Signs That Tokens Need Updating

- **403 Forbidden errors** in the scraper
- **"Access forbidden. Credentials may be expired"** in logs
- **Empty results** when there should be posts
- **Rate limiting that doesn't resolve**

## 🛡️ Security Tips

1. **Never share tokens publicly** - they give access to your LinkedIn account
2. **Update tokens regularly** - don't wait for expiration
3. **Use a dedicated LinkedIn account** for scraping if possible
4. **Monitor for unusual activity** on your LinkedIn account

## 📱 Mobile App vs Web Tokens

- **Mobile app tokens** (from Android/iOS) tend to last longer
- **Web browser tokens** expire more frequently
- **The current config uses mobile app format** for better stability

## 🔄 Automation Ideas

For advanced users, you could:
1. Create a script to auto-extract tokens from browser storage
2. Set up automated token refresh
3. Use multiple accounts with token rotation

## 💡 Troubleshooting

**Q: I get 403 errors immediately**
A: Your `li_at` or `csrf-token` is expired. Update both.

**Q: Scraper works but gets no results**
A: Your search terms might be too specific, or the `PAGE_INSTANCE` needs updating.

**Q: Rate limited constantly**
A: Increase `BASE_DELAY` in config or wait longer between runs.

**Q: Tokens expire quickly**
A: Use mobile app tokens instead of web browser tokens.

## 📞 Quick Token Check

Run the scraper - it will show you the first 20-30 characters of each token so you can verify they're being used correctly.

---

*Remember: Keep your tokens secure and update them when they expire!* 