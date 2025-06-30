#!/usr/bin/env python3
"""
LinkedIn API Call Script - Enhanced Version
Features: Rate limiting, User agent rotation, Error handling, Anti-detection, Message sending
Uses GraphQL endpoint for clean structured data extraction and messaging API for sending messages
"""

import requests
import json
import csv
import time
import random
from datetime import datetime
import urllib.parse
from typing import Dict, List, Optional
import logging
import uuid

# ==========================================
# CONFIGURATION SETTINGS - EDIT THESE VALUES
# ==========================================

# Search settings
SEARCH_KEYWORDS = "hiring marketing dubai"  # What you want to search for
TARGET_POSTS = 40                          # How many posts you want (total)
POSTS_PER_PAGE = 10                        # Posts to fetch per page (recommended: 10)
MAX_PAGES = 6                              # Maximum pages to fetch (safety limit)

# Messaging settings
MESSAGE_DELAY = 5                          # Delay between messages (seconds)
MAX_MESSAGES_PER_SESSION = 50              # Maximum messages per session (safety limit)
DEFAULT_MESSAGE = "Hi there! I came across your profile and would love to connect. Looking forward to networking with you!"

# Rate limiting settings (to avoid being blocked)
BASE_DELAY = 2                             # Base delay between requests (seconds)
MAX_RETRIES = 3                           # Maximum retry attempts per request
REQUEST_TIMEOUT = 30                      # Request timeout (seconds)

# Output settings
OUTPUT_PREFIX = "linkedin_search_results"  # Prefix for output files
ENABLE_LOGGING = True                     # Enable detailed logging

# ==========================================
# AUTHENTICATION SETTINGS - IMPORTED FROM CONFIG
# ==========================================

# Import sensitive authentication data from separate config file
try:
    from config import (
        CSRF_TOKEN, JSESSIONID, LI_AT_TOKEN, LI_RM_TOKEN,
        BCOOKIE, BSCOOKIE, LIDC_COOKIE, PAGE_INSTANCE, QUERY_ID
    )
    print("✅ Authentication config loaded successfully")
except ImportError:
    print("❌ ERROR: config.py not found!")
    print("📋 Please copy config_template.py to config.py and add your LinkedIn tokens")
    print("📖 See linkedin_auth_guide.md for instructions on getting tokens")
    exit(1)

# ==========================================
# END OF CONFIGURATION
# ==========================================

# Configure logging
if ENABLE_LOGGING:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('linkedin_scraper.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
else:
    logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)

class LinkedInScraper:
    """Enhanced LinkedIn scraper with anti-detection measures and messaging capabilities"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_delay = BASE_DELAY  # Base delay between requests in seconds
        self.max_retries = MAX_RETRIES
        self.timeout = REQUEST_TIMEOUT
        
        # User agent rotation for anti-detection
        self.user_agents = [
            'com.linkedin.android/199600 (Linux; U; Android 13; en_US; sdk_gphone64_x86_64; Build/TE1A.240213.009; Cronet/127.0.6533.65)',
            'com.linkedin.android/199500 (Linux; U; Android 12; en_US; Pixel 6; Build/SD1A.210817.036; Cronet/127.0.6533.64)',
            'com.linkedin.android/199400 (Linux; U; Android 11; en_US; SM-G991B; Build/RP1A.200720.012; Cronet/127.0.6533.63)',
            'com.linkedin.android/199300 (Linux; U; Android 13; en_US; OnePlus 9; Build/RKQ1.201105.002; Cronet/127.0.6533.62)'
        ]
        
        # Web user agents for messaging
        self.web_user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        ]
        
        # Device IDs for rotation
        self.device_ids = [
            'de49e77d-1fc7-423b-9501-585fbe60dff9',
            'af38b98c-2ed8-534a-a412-696cdf71eaa8',
            'bc27c8df-3fa9-445b-b523-807def82cbc9',
            'cd16d7ee-4gb0-556c-c634-918aef93dcd0'
        ]
        
        # Base headers template
        self.base_headers = {
            'x-restli-protocol-version': '2.0.0',
            'x-li-graphql-pegasus-client': 'true',
            'accept-language': 'en-US',
            'csrf-token': CSRF_TOKEN,
            'x-li-page-instance': PAGE_INSTANCE,
            'x-li-pem-metadata': 'Voyager - Content SRP=search-results',
            'x-restli-symbol-table-name': 'voyager-21304',
            'x-li-lang': 'en_US',
            'accept': 'application/json',
            'cookie': f"JSESSIONID={JSESSIONID}; bcookie={BCOOKIE}; bscookie={BSCOOKIE}; lang=v=2&lang=en_US; li_at={LI_AT_TOKEN}; li_rm={LI_RM_TOKEN}; liap=true; lidc={LIDC_COOKIE}",
            'priority': 'u=0, i'
        }
        
        # Messaging headers template
        self.messaging_headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'csrf-token': CSRF_TOKEN,
            'origin': 'https://www.linkedin.com',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'x-li-lang': 'en_US',
            'x-restli-protocol-version': '2.0.0',
            'cookie': f"bcookie={BCOOKIE}; bscookie={BSCOOKIE}; liap=true; JSESSIONID={JSESSIONID}; timezone=Asia/Dubai; li_theme=light; li_theme_set=app; li_at={LI_AT_TOKEN}; lang=v=2&lang=en-us; lidc={LIDC_COOKIE}"
        }
    
    def get_random_headers(self, for_messaging: bool = False) -> Dict[str, str]:
        """Generate randomized headers for anti-detection"""
        if for_messaging:
            headers = self.messaging_headers.copy()
            headers['user-agent'] = random.choice(self.web_user_agents)
            
            # Generate web tracking data
            track_data = {
                "clientVersion": "1.13.36800.3",
                "mpVersion": "1.13.36800.3",
                "osName": "web",
                "timezoneOffset": 4,
                "timezone": "Asia/Dubai",
                "deviceFormFactor": "DESKTOP",
                "mpName": "voyager-web",
                "displayDensity": random.choice([2.0, 2.5, 3.0]),
                "displayWidth": random.choice([1920, 2560, 3440]),
                "displayHeight": random.choice([1080, 1440, 1600])
            }
            
            headers['x-li-track'] = json.dumps(track_data)
            return headers
        else:
            headers = self.base_headers.copy()
            
            # Rotate user agent
            headers['user-agent'] = random.choice(self.user_agents)
            
            # Rotate device ID
            device_id = random.choice(self.device_ids)
            headers['x-udid'] = device_id
            
            # Generate tracking data with rotated device ID
            track_data = {
                "osName": "Android OS",
                "osVersion": random.choice(["13", "12", "11"]),
                "clientVersion": "4.1.1088",
                "clientMinorVersion": random.randint(199300, 199600),
                "model": random.choice([
                    "Google_sdk_gphone64_x86_64",
                    "Pixel 6",
                    "SM-G991B",
                    "OnePlus 9"
                ]),
                "displayDensity": random.choice([3.0, 3.5, 4.0]),
                "displayWidth": random.choice([1440, 1080, 1200]),
                "displayHeight": random.choice([2891, 2340, 2400]),
                "dpi": "xhdpi",
                "deviceType": "android",
                "appId": "com.linkedin.android",
                "deviceId": device_id,
                "timezoneOffset": 4,
                "timezone": "Asia/Dubai",
                "storeId": "us_googleplay",
                "isAdTrackingLimited": False,
                "mpName": "voyager-android",
                "mpVersion": "2.166.40"
            }
            
            headers['x-li-track'] = json.dumps(track_data)
            return headers
    
    def apply_rate_limiting(self, attempt: int = 0, is_messaging: bool = False) -> None:
        """Apply intelligent rate limiting with exponential backoff"""
        if is_messaging:
            delay = MESSAGE_DELAY + random.uniform(1.0, 3.0)
        elif attempt == 0:
            delay = self.base_delay + random.uniform(0.5, 2.0)
        else:
            # Exponential backoff for retries
            delay = self.base_delay * (2 ** attempt) + random.uniform(1.0, 3.0)
        
        logger.info(f"Applying rate limit: {delay:.2f} seconds")
        time.sleep(delay)
    
    def send_message(self, conversation_urn: str, message_text: str, mailbox_urn: str = None) -> bool:
        """Send a message to a LinkedIn conversation"""
        url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage"
        
        # Generate unique tokens
        origin_token = str(uuid.uuid4())
        tracking_id = str(uuid.uuid4())[:16]
        
        # If mailbox_urn is not provided, try to extract from conversation_urn
        if not mailbox_urn:
            # This is a simplified extraction - you might need to adjust based on actual URN format
            if "urn:li:fsd_profile:" in conversation_urn:
                mailbox_urn = conversation_urn.split(",")[0].replace("urn:li:msg_conversation:(", "")
            else:
                logger.error("Could not extract mailbox URN from conversation URN")
                return False
        
        payload = {
            "message": {
                "body": {
                    "attributes": [],
                    "text": message_text
                },
                "renderContentUnions": [],
                "conversationUrn": conversation_urn,
                "originToken": origin_token
            },
            "mailboxUrn": mailbox_urn,
            "trackingId": tracking_id,
            "dedupeByClientGeneratedToken": False
        }
        
        for attempt in range(self.max_retries):
            try:
                # Apply rate limiting for messaging
                if attempt > 0:
                    self.apply_rate_limiting(attempt, is_messaging=True)
                else:
                    self.apply_rate_limiting(is_messaging=True)
                
                # Get messaging headers
                headers = self.get_random_headers(for_messaging=True)
                
                logger.info(f"Sending message (attempt: {attempt + 1})")
                logger.info(f"Message: {message_text[:50]}...")
                
                response = self.session.post(
                    url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=self.timeout
                )
                
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    logger.info("✅ Message sent successfully!")
                    return True
                elif response.status_code == 429:
                    logger.warning("Rate limited by LinkedIn. Waiting longer...")
                    time.sleep(60 + random.uniform(10, 30))
                    continue
                elif response.status_code == 403:
                    logger.error("Access forbidden. Credentials may be expired or insufficient permissions.")
                    break
                else:
                    logger.warning(f"Unexpected status code: {response.status_code}")
                    logger.debug(f"Response: {response.text[:500]}...")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    self.apply_rate_limiting(attempt, is_messaging=True)
                    continue
                else:
                    break
        
        logger.error("❌ Failed to send message after all attempts")
        return False
    
    def send_bulk_messages(self, recipients: List[Dict], message_text: str = None) -> Dict:
        """Send messages to multiple recipients"""
        if not message_text:
            message_text = DEFAULT_MESSAGE
        
        results = {
            'success': 0,
            'failed': 0,
            'total': len(recipients),
            'failed_recipients': []
        }
        
        logger.info(f"Starting bulk message sending to {len(recipients)} recipients")
        
        for i, recipient in enumerate(recipients, 1):
            if results['success'] >= MAX_MESSAGES_PER_SESSION:
                logger.warning(f"Reached maximum messages per session ({MAX_MESSAGES_PER_SESSION}). Stopping.")
                break
            
            conversation_urn = recipient.get('conversation_urn')
            mailbox_urn = recipient.get('mailbox_urn')
            recipient_name = recipient.get('name', 'Unknown')
            
            if not conversation_urn:
                logger.error(f"No conversation URN for recipient {i}: {recipient_name}")
                results['failed'] += 1
                results['failed_recipients'].append(recipient)
                continue
            
            logger.info(f"Sending message {i}/{len(recipients)} to {recipient_name}")
            
            success = self.send_message(conversation_urn, message_text, mailbox_urn)
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
                results['failed_recipients'].append(recipient)
        
        return results
    
    def make_api_call(self, start_page: int = 0, count: int = 10) -> Optional[Dict]:
        """Make LinkedIn API call with retry logic and error handling"""
        keywords = SEARCH_KEYWORDS
        
        # Build URL with proper encoding
        base_url = "https://www.linkedin.com/voyager/api/graphql"
        variables = f"(query:(flagshipSearchIntent:SEARCH_SRP,includeFiltersInResponse:false,keywords:{urllib.parse.quote(keywords)},queryParameters:(resultType:List(CONTENT),sortBy:List(date_posted)),spellCorrectionEnabled:true),origin:GLOBAL_SEARCH_HEADER,count:{count},start:{start_page})"
        query_name = "SearchClusterCollection"
        query_id = QUERY_ID
        
        url = f"{base_url}?variables={variables}&queryName={query_name}&queryId={query_id}"
        
        for attempt in range(self.max_retries):
            try:
                # Apply rate limiting
                if attempt > 0:
                    self.apply_rate_limiting(attempt)
                
                # Get randomized headers
                headers = self.get_random_headers()
                
                logger.info(f"Making API call (page: {start_page//10 + 1}, attempt: {attempt + 1})")
                
                response = self.session.get(
                    url, 
                    headers=headers, 
                    timeout=self.timeout
                )
                
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    # Rate limited - wait longer
                    logger.warning("Rate limited by LinkedIn. Waiting longer...")
                    time.sleep(60 + random.uniform(10, 30))
                    continue
                elif response.status_code == 403:
                    logger.error("Access forbidden. Credentials may be expired.")
                    break
                else:
                    logger.warning(f"Unexpected status code: {response.status_code}")
                    logger.debug(f"Response: {response.text[:500]}...")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    self.apply_rate_limiting(attempt)
                    continue
                else:
                    break
        
        return None
    
    @staticmethod
    def clean_profile_url(url: str) -> str:
        """Clean profile URL by removing query parameters"""
        if not url or 'URL not found' in url:
            return url
        
        # For individual profiles, clean up the URL
        if '/in/' in url and '?' in url:
            return url.split('?')[0]
        
        return url
    
    def extract_posts_from_json(self, json_data: Dict) -> List[Dict]:
        """Extract posts data from the structured JSON response"""
        posts = []
        
        try:
            elements = json_data.get('data', {}).get('searchDashClustersByAll', {}).get('elements', [])
            
            for element in elements:
                items = element.get('items', [])
                for item_wrapper in items:
                    item = item_wrapper.get('item', {})
                    
                    search_feed_update = item.get('searchFeedUpdate')
                    if search_feed_update:
                        update = search_feed_update.get('update', {})
                        if update:
                            post_data = self._extract_post_data(update)
                            
                            # Only add posts with meaningful content
                            if post_data.get('post_content') and post_data.get('author_name'):
                                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            logger.error(f"Error extracting posts: {e}")
            return []
    
    def _extract_post_data(self, update: Dict) -> Dict:
        """Extract individual post data from update object"""
        post_data = {}
        
        # Extract actor (author) information
        actor = update.get('actor', {})
        if actor:
            name_obj = actor.get('name', {})
            if name_obj:
                post_data['author_name'] = name_obj.get('text', 'Unknown')
            
            nav_context = actor.get('navigationContext', {})
            if nav_context:
                action_target = nav_context.get('actionTarget', '')
                post_data['profile_url'] = self.clean_profile_url(action_target)
            else:
                post_data['profile_url'] = 'URL not found'
        
        # Extract post content from commentary
        commentary = update.get('commentary', {})
        if commentary:
            text_obj = commentary.get('text', {})
            if text_obj:
                post_data['post_content'] = text_obj.get('text', '')
        
        # Extract social content for post URL
        social_content = update.get('socialContent', {})
        if social_content:
            post_data['post_url'] = social_content.get('shareUrl', '')
        
        return post_data
    
    def save_to_csv(self, posts: List[Dict], filename_prefix: str = OUTPUT_PREFIX) -> Optional[str]:
        """Save posts to CSV file with UTF-8 encoding"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{filename_prefix}_{timestamp}.csv"
        
        headers = ['Post_Number', 'Author_Name', 'Profile_URL', 'Post_Content', 'Post_URL']
        
        try:
            with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                
                for i, post in enumerate(posts, 1):
                    row = [
                        i,
                        post.get('author_name', 'Unknown'),
                        post.get('profile_url', 'Not found'),
                        post.get('post_content', 'No content'),
                        post.get('post_url', 'No URL')
                    ]
                    writer.writerow(row)
            
            logger.info(f"[SUCCESS] CSV file saved with UTF-8 encoding: {csv_filename}")
            return csv_filename
            
        except Exception as e:
            logger.error(f"[ERROR] Error saving CSV: {e}")
            return None
    
    def save_backup_files(self, raw_data: Dict, posts: List[Dict], filename_prefix: str = OUTPUT_PREFIX) -> tuple:
        """Save backup files (JSON and TXT)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save raw JSON
        raw_filename = f"{filename_prefix}_raw_{timestamp}.json"
        try:
            with open(raw_filename, 'w', encoding='utf-8') as f:
                json.dump(raw_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Raw data saved: {raw_filename}")
        except Exception as e:
            logger.error(f"Error saving raw data: {e}")
            raw_filename = None
        
        # Save parsed TXT
        parsed_filename = f"{filename_prefix}_parsed_{timestamp}.txt"
        try:
            with open(parsed_filename, 'w', encoding='utf-8') as f:
                f.write("=== LinkedIn Marketing Jobs in Dubai ===\n\n")
                
                for i, post in enumerate(posts, 1):
                    f.write(f"POST #{i}\n")
                    f.write("-" * 50 + "\n")
                    f.write(f"Author: {post.get('author_name', 'Unknown')}\n")
                    f.write(f"Profile: {post.get('profile_url', 'Not found')}\n")
                    f.write(f"Content: {post.get('post_content', 'No content')}\n")
                    f.write(f"URL: {post.get('post_url', 'No URL')}\n")
                    f.write("\n")
            
            logger.info(f"Parsed results saved: {parsed_filename}")
        except Exception as e:
            logger.error(f"Error saving parsed results: {e}")
            parsed_filename = None
        
        return raw_filename, parsed_filename
    
    def scrape_posts(self, target_posts: int = TARGET_POSTS, posts_per_page: int = POSTS_PER_PAGE) -> List[Dict]:
        """Main scraping function with intelligent pagination"""
        logger.info(f"[START] LinkedIn scraper - Target: {target_posts} posts")
        
        all_posts = []
        page = 0
        consecutive_empty_pages = 0
        max_empty_pages = 2
        max_pages = MAX_PAGES  # Safety limit
        
        while len(all_posts) < target_posts and page < max_pages:
            start_page = page * posts_per_page
            
            logger.info(f"[PAGE] Fetching page {page + 1} (posts: {start_page}-{start_page + posts_per_page - 1})")
            
            # Apply rate limiting before each request
            if page > 0:
                self.apply_rate_limiting()
            
            json_data = self.make_api_call(start_page=start_page, count=posts_per_page)
            
            if json_data:
                posts = self.extract_posts_from_json(json_data)
                
                if posts:
                    all_posts.extend(posts)
                    consecutive_empty_pages = 0
                    logger.info(f"[SUCCESS] Found {len(posts)} posts. Total: {len(all_posts)}")
                else:
                    consecutive_empty_pages += 1
                    logger.warning(f"No posts found on page {page + 1}")
                    
                    if consecutive_empty_pages >= max_empty_pages:
                        logger.info("Multiple empty pages detected. Stopping.")
                        break
            else:
                logger.error(f"[ERROR] API call failed for page {page + 1}")
                break
            
            page += 1
        
        # Limit to target number of posts
        if len(all_posts) > target_posts:
            all_posts = all_posts[:target_posts]
            logger.info(f"Limited results to {target_posts} posts as requested")
        
        return all_posts

def main():
    """Main execution function"""
    try:
        # Display current configuration
        print("=" * 60)
        print("🔍 LINKEDIN SCRAPER - CURRENT CONFIGURATION")
        print("=" * 60)
        print(f"📝 Search Keywords: '{SEARCH_KEYWORDS}'")
        print(f"📊 Target Posts: {TARGET_POSTS}")
        print(f"📄 Posts per Page: {POSTS_PER_PAGE}")
        print(f"🔢 Max Pages: {MAX_PAGES}")
        print(f"⏱️  Rate Limit: {BASE_DELAY}s base delay")
        print(f"📁 Output Prefix: '{OUTPUT_PREFIX}'")
        print()
        print("🔐 AUTHENTICATION STATUS")
        print("-" * 30)
        print(f"🔑 CSRF Token: {CSRF_TOKEN[:20]}...")
        print(f"🍪 Session ID: {JSESSIONID[:20]}...")
        print(f"👤 LI_AT Token: {LI_AT_TOKEN[:30]}...")
        print(f"🔒 LI_RM Token: {LI_RM_TOKEN[:30]}...")
        print(f"📄 Page Instance: {PAGE_INSTANCE[:40]}...")
        print(f"🔍 Query ID: {QUERY_ID[:40]}...")
        print("=" * 60)
        print()
        
        scraper = LinkedInScraper()
        
        # Scrape posts
        posts = scraper.scrape_posts(target_posts=TARGET_POSTS)
        
        if posts:
            logger.info(f"[COMPLETE] Successfully scraped {len(posts)} posts!")
            
            # Save to CSV
            csv_file = scraper.save_to_csv(posts)
            
            # Save backup files (use the last successful API response)
            # For simplicity, we'll just save the parsed results
            raw_file, parsed_file = scraper.save_backup_files({}, posts)
            
            # Show sample results
            logger.info("[SAMPLE] Sample Results (first 3 posts):")
            for i, post in enumerate(posts[:3], 1):
                logger.info(f"\nPost #{i}:")
                logger.info(f"Author: {post.get('author_name', 'Unknown')}")
                logger.info(f"Profile: {post.get('profile_url', 'Not found')}")
                logger.info(f"Content: {post.get('post_content', 'No content')[:100]}...")
            
            print("\n" + "=" * 60)
            print("✅ SCRAPING COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"📊 CSV File: {csv_file}")
            print(f"📄 Text File: {parsed_file}")
            print(f"📝 Total Posts: {len(posts)}")
            print(f"🔍 Search: '{SEARCH_KEYWORDS}'")
            print("=" * 60)
            
        else:
            logger.error("[ERROR] No posts found!")
            print("\n❌ No posts found!")
            print("💡 This might be due to:")
            print("   • Expired authentication tokens")
            print("   • Rate limiting by LinkedIn")
            print("   • No results for your search terms")
            print("   • Network connectivity issues")
            print("\n🔧 Try updating the authentication tokens in the config section!")
            
    except KeyboardInterrupt:
        logger.info("[STOP] Scraping interrupted by user")
        print("\n⏹️ Scraping stopped by user.")
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        print(f"\n💥 Error occurred: {e}")
        if "403" in str(e) or "Forbidden" in str(e):
            print("🔧 This looks like an authentication error. Try updating your tokens!")

if __name__ == "__main__":
    main() 