# LinkedIn Connection Checker

This script checks if a given LinkedIn profile is connected with you by analyzing the connection distance through LinkedIn's voyager API.

## 🔗 Connection Distance Explained

- **Distance 1**: Direct connection (1st degree) - You are connected
- **Distance 2**: 2nd degree connection (friend of a friend)
- **Distance 3**: 3rd degree or extended network
- **Distance None/0**: Not connected or profile not accessible

## 🔐 Authentication Methods

### Your Example (Bearer Token)
```python
token = "Your-Token-Here"
headers = {"Authorization": f"Bearer {token}"}
```

### Our Implementation (Cookie-based)
```python
cookies = {
    "li_at": "AQEDASP6v4E...",
    "JSESSIONID": "ajax:476328...",
    # ... more cookies
}
```

### Why Cookie-based Authentication?

1. **More Reliable**: LinkedIn's web interface uses cookie-based auth
2. **No Token Management**: Cookies are extracted from browser sessions
3. **Better Success Rate**: Works with the same endpoints as the web interface
4. **Session Persistence**: Maintains state across multiple requests

## 📁 Files Overview

### `linkedin_connection_checker.py`
Main script with the `LinkedInConnectionChecker` class. Features:
- Multiple API endpoint attempts for maximum success rate
- Robust error handling and fallback methods
- Profile name extraction
- Connection distance detection

### `example_connection_check.py`
Example usage showing both simple function calls and advanced class usage.

## 🚀 Usage Examples

### Simple Usage
```python
from linkedin_connection_checker import check_connection

result = check_connection("https://www.linkedin.com/in/johndoe/")
if result['is_connected']:
    print(f"Connected with {result['profile_name']}")
```

### Advanced Usage
```python
from linkedin_connection_checker import LinkedInConnectionChecker

checker = LinkedInConnectionChecker()
result = checker.check_connection_status(profile_url)

print(f"Distance: {result['distance']}")
print(f"Status: {result['connection_status']}")
```

### Command Line Usage
```bash
python linkedin_connection_checker.py "https://www.linkedin.com/in/johndoe/"
```

## 🔧 How It Works

### 1. URL Processing
- Extracts public identifier from LinkedIn URL
- Handles various URL formats (with/without https, trailing slashes, etc.)

### 2. Multiple API Attempts
The script tries different LinkedIn API endpoints in order:

1. **profileView endpoint**: Most direct method
   ```
   /voyager/api/identity/profiles/{public_id}/profileView
   ```

2. **Identity API**: General profile information
   ```
   /voyager/api/identity/profiles/{public_id}
   ```

3. **Contact Info endpoint**: Often contains connection data
   ```
   /voyager/api/identity/profiles/{urn_id}/profileContactInfo
   ```

### 3. Connection Detection Methods
- **Direct distance field**: `data.distance.distance`
- **Text analysis**: Searches for "connected", "1st", "2nd", "3rd" keywords
- **Messaging availability**: Connected users can usually message each other
- **Included elements**: Checks nested data structures

## 📊 Response Structure

```python
{
    "profile_url": "https://www.linkedin.com/in/johndoe/",
    "is_connected": True,
    "distance": 1,
    "connection_status": "1st degree - Direct connection",
    "profile_name": "John Doe",
    "error": None,
    "source": "profileView"
}
```

## 🔄 Authentication Setup

### Getting Your Cookies

1. **Login to LinkedIn** in your browser
2. **Open Developer Tools** (F12)
3. **Go to Network tab**
4. **Visit any LinkedIn page**
5. **Find a request to linkedin.com**
6. **Copy cookies from Request Headers**

### Important Cookies
- `li_at`: Main authentication token
- `JSESSIONID`: Session identifier
- `csrf-token`: Cross-site request forgery protection

### Updating the Script
Replace the cookies in the `setup_session()` method:

```python
cookies = {
    "li_at": "YOUR_LI_AT_COOKIE",
    "JSESSIONID": "YOUR_JSESSIONID",
    # ... other cookies
}
```

## ⚠️ Important Notes

### Rate Limiting
- LinkedIn has rate limits on API requests
- The script includes delays and error handling
- Don't make too many requests in short time periods

### Cookie Expiration
- Cookies expire periodically (usually 30-90 days)
- You'll need to update them when they expire
- The script will show authentication errors when cookies are invalid

### Legal Considerations
- Use responsibly and respect LinkedIn's Terms of Service
- Don't use for spamming or unauthorized data collection
- Consider using LinkedIn's official APIs for commercial applications

## 🐛 Troubleshooting

### Common Issues

1. **"Could not extract public identifier"**
   - Check if the LinkedIn URL is correct
   - Try with different URL formats

2. **"ProfileView endpoint failed: 401"**
   - Your cookies are expired or invalid
   - Update the cookies in `setup_session()`

3. **"Could not determine connection status"**
   - The profile might be private
   - LinkedIn might be blocking the request
   - Try with a different profile

### Debug Mode
Add print statements to see the raw API responses:

```python
response = self.session.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}...")  # First 500 chars
```

## 🔄 Updates and Maintenance

LinkedIn frequently updates their APIs and authentication methods. You may need to:

1. **Update cookies** regularly
2. **Modify API endpoints** if LinkedIn changes them
3. **Adjust headers** to match current browser requests
4. **Update parsing logic** if response structure changes

## 📈 Extending the Script

### Adding More Endpoints
```python
def check_via_new_endpoint(self, public_id: str) -> Optional[Dict]:
    url = f"https://www.linkedin.com/voyager/api/new/endpoint/{public_id}"
    # ... implementation
```

### Custom Connection Logic
```python
def custom_connection_check(self, data: Dict) -> bool:
    # Your custom logic here
    return True  # or False
```

### Batch Processing
```python
def check_multiple_profiles(self, urls: List[str]) -> List[Dict]:
    results = []
    for url in urls:
        result = self.check_connection_status(url)
        results.append(result)
        time.sleep(1)  # Rate limiting
    return results
``` 