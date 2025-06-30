import requests
import json
import re
import uuid
import html
from typing import Optional, Tuple
from linkedin_conversation_extractor import LinkedInConversationExtractor  # NEW IMPORT

# ==========================================
# AUTOMATION FUNCTIONS FOR LINKEDIN URNS
# ==========================================

def clean_urn(urn: str) -> str:
    """Clean URN by removing HTML entities and unwanted characters."""
    if not urn:
        return urn
    
    # Remove HTML entities
    urn = html.unescape(urn)
    
    # Remove quotes and other unwanted characters at the end
    urn = re.sub(r'["\'\s&;]+$', '', urn)
    
    return urn

def extract_profile_urn_from_url(profile_url: str) -> Optional[str]:
    """
    Extract LinkedIn profile URN from profile URL.
    
    Args:
        profile_url: LinkedIn profile URL (e.g., https://www.linkedin.com/in/john-doe/)
    
    Returns:
        Profile URN in format: urn:li:fsd_profile:XXXXXX or None if not found
    """
    try:
        # Create session for URN resolution
        session = requests.Session()
        session.cookies.update(cookies)
        
        # If already a URN, clean and return it
        if profile_url.startswith('urn:li:fsd_profile:'):
            return clean_urn(profile_url)
        
        print(f"🔍 Resolving URN for: {profile_url}")
        
        # Method 1: Try to get profile data from the profile page
        profile_headers = headers.copy()
        profile_headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'referer': 'https://www.linkedin.com/',
        })
        
        response = session.get(profile_url, headers=profile_headers)
        
        if response.status_code == 200:
            # Look for profile URN in the page source with multiple patterns
            urn_patterns = [
                r'"urn:li:fsd_profile:([^"]+)"',
                r'urn:li:fsd_profile:([^,)"\s&]+)',
                r'"profileUrn":"urn:li:fsd_profile:([^"]+)"',
                r'&quot;urn:li:fsd_profile:([^&]+)&quot;',
                r'%22urn:li:fsd_profile:([^%]+)%22',
            ]
            
            for pattern in urn_patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    urn_id = matches[0]
                    full_urn = f"urn:li:fsd_profile:{urn_id}"
                    cleaned_urn = clean_urn(full_urn)
                    print(f"✅ Found URN: {cleaned_urn}")
                    return cleaned_urn
        
        # Method 2: Fallback to username extraction
        print("🔄 Using username fallback method...")
        username = profile_url.split('/in/')[-1].strip('/')
        
        # This is simplified - for actual messaging you need the full encoded URN
        return f"urn:li:fsd_profile:{username}"
        
    except Exception as e:
        print(f"❌ Error extracting profile URN: {e}")
        return None

def search_conversations(session: requests.Session, profile_urn: str) -> Optional[str]:
    """
    Search for existing conversations with a specific profile.
    
    Args:
        session: Authenticated requests session
        profile_urn: Profile URN to search conversations for
    
    Returns:
        Conversation URN if found, None otherwise
    """
    try:
        # LinkedIn conversations API endpoint
        url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashConversations"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "csrf-token": "ajax:4763283604314235653",
            "x-li-lang": "en_US",
            "x-restli-protocol-version": "2.0.0",
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.7",
        }
        
        # Search for conversations
        response = session.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Search through conversations for matching profile
            conversations = data.get('elements', [])
            for conv in conversations:
                participants = conv.get('participants', [])
                for participant in participants:
                    if profile_urn in str(participant):
                        return conv.get('entityUrn', '')
        
        return None
    except Exception as e:
        print(f"Error searching conversations: {e}")
        return None

def create_conversation_urn(profile_urn: str, conversation_id: str = None) -> str:
    """
    Create a conversation URN for messaging.
    
    Args:
        profile_urn: The recipient's profile URN
        conversation_id: Optional conversation ID, generates random if not provided
    
    Returns:
        Formatted conversation URN
    """
    if not conversation_id:
        # Generate a random conversation ID (simplified)
        conversation_id = "2-" + str(uuid.uuid4()).replace('-', '')[:32]
    
    return f"urn:li:msg_conversation:({profile_urn},{conversation_id})"

def get_linkedin_urns(profile_url_or_urn: str, session: requests.Session = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Automatically get mailboxUrn and conversationUrn for LinkedIn messaging.
    
    Args:
        profile_url_or_urn: LinkedIn profile URL or URN
        session: Optional authenticated session for conversation search
    
    Returns:
        Tuple of (mailboxUrn, conversationUrn)
    """
    # Extract and clean profile URN
    if profile_url_or_urn.startswith('urn:li:fsd_profile:'):
        mailbox_urn = clean_urn(profile_url_or_urn)
    else:
        mailbox_urn = extract_profile_urn_from_url(profile_url_or_urn)
        if mailbox_urn:
            mailbox_urn = clean_urn(mailbox_urn)
    
    if not mailbox_urn:
        print("❌ Could not extract profile URN")
        return None, None
    
    # Try to find existing conversation (LinkedIn requires existing conversations)
    conversation_urn = None
    if session:
        conversation_urn = search_conversations(session, mailbox_urn)
        if conversation_urn:
            print("✅ Found existing conversation")
    
    # LinkedIn doesn't allow creating new conversations via API
    # Return None for conversation_urn if no existing conversation found
    # The calling code should use known working conversation URNs as fallback
    if not conversation_urn:
        print("❌ No existing conversation found. You can only message existing conversations.")
        print("💡 Use LinkedIn web interface to start a conversation first, then get the conversation URN.")
    
    return mailbox_urn, conversation_urn

# ==========================================
# ORIGINAL AUTHENTICATION AND HEADERS
# ==========================================

# Define cookies (use a full, clean set as in your example)
cookies = {
    "bcookie": "v=2&12e9e7e4-3797-4b9d-8b85-e67c6fbbcf80",
    "li_sugr": "9c83b1f7-b3ab-47d6-8f9c-aac27e761ba1",
    "bscookie": "v=1&20250507140639ea67aaf7-6f73-48ff-8813-9f6383cea24eAQEBEVVX01KNZ7vWOUKdmFDVKvhshdNt",
    "liap": "true",
    "JSESSIONID": "ajax:4763283604314235653",
    "_guid": "c4c27323-6441-4b94-8a60-e2dae58ecd41",
    "dfpfpt": "3c04e81e591e469e8cf3481efad5f950",
    "timezone": "Asia/Dubai",
    "li_theme": "light",
    "li_theme_set": "app",
    "li_at": "AQEDASP6v4EBfhJ7AAABl8BT3OQAAAGX5GBg5E0AocvtLBfU2unQg6KLYHNi6AG83PSJwqQdkZ2kcjhYnS0jlwh0Xy834jLziuj_Kdg3yOwz-L-QrbzlBOjMqHho03KrmOqhKNRdfYXUPajAOyj_oUg_",
    "lang": "v=2&lang=en-us",
    "AnalyticsSyncHistory": "AQLwTYiBPPXAEQAAAZeq9LsZodIRFt_Zyzisf1c3QnUwif1sDC0AaLlviE-azQevBEOVyvdiwPqNY36wV-xZxw",
    "fptctx2": "....",  # Shortened for brevity; use your full value
    "sdui_ver": "sdui-flagship:0.1.7528+sdui-flagship.production",
    "lms_ads": "....",
    "lms_analytics": "....",
    "UserMatchHistory": "....",
    "lidc": "b=VB85:s=V:r=V:a=V:p=V:g=5950:u=785:x=1:i=1751116112:t=1751157469:v=2:sig=AQHO7kkYm6_UVNy5H4OrCoar7zLfZY5w"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "csrf-token": "ajax:4763283604314235653",
    "x-li-lang": "en_US",
    "x-li-page-instance": "urn:li:page:d_flagship3_messaging_conversation_detail;WlIOZhHvTp2Ya52EhsXI1Q==",
    "x-li-track": '{"clientVersion":"1.13.36800.3","mpVersion":"1.13.36800.3","osName":"web","timezoneOffset":4,"timezone":"Asia/Dubai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2.5,"displayWidth":3600,"displayHeight":2250}',
    "x-restli-protocol-version": "2.0.0",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.7",
    "referer": "https://www.linkedin.com/messaging/thread/2-OTkxOWNhY2YtYWY1ZC00OTNjLWE5YzItMmZiYjFhYzE2MjE1XzEwMA==/",
    "origin": "https://www.linkedin.com",
    "content-type": "text/plain;charset=UTF-8"
}

# ==========================================
# AUTOMATED URN EXTRACTION
# ==========================================

# Create session with cookies
session = requests.Session()
session.cookies.update(cookies)

# Initialize URNs as None - will be set via name lookup
mailbox_urn = None
conversation_urn = None

# ==========================================
# SEND MESSAGE WITH AUTOMATED URNS
# ==========================================

def send_linkedin_message(message_text: str, target_profile: str) -> bool:
    """
    Send a LinkedIn message with automatic URN extraction.
    
    Args:
        message_text: The message to send
        target_profile: LinkedIn profile URL or URN
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get URNs
        mailbox_urn, conversation_urn = get_linkedin_urns(target_profile, session)
        
        if not mailbox_urn or not conversation_urn:
            print("❌ Could not get LinkedIn URNs")
            return False
        
        # Prepare payload
        payload = {
            "message": {
                "body": {
                    "attributes": [],
                    "text": message_text
                },
                "renderContentUnions": [],
                "conversationUrn": conversation_urn,
                "originToken": str(uuid.uuid4())
            },
            "mailboxUrn": mailbox_urn,
            "trackingId": str(uuid.uuid4())[:16],
            "dedupeByClientGeneratedToken": False
        }
        
        # Send message
        url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage"
        response = session.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            print("✅ Message sent successfully!")
            return True
        else:
            print(f"❌ Failed to send message. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

# ==========================================
# SEND THE MESSAGE DIRECTLY
# ==========================================

if __name__ == "__main__":
    # NEW: Ask user for recipient's name and resolve URNs automatically
    input_value = input("👤 Enter the recipient's name OR LinkedIn profile URL (e.g., 'oussama' or 'https://www.linkedin.com/in/oussamagaham/'): ").strip()
    if input_value:
        try:
            extractor = LinkedInConversationExtractor()
            result = extractor.get_urns_by_name(input_value)
            if result:
                mailbox_urn = result["mailbox_urn"]
                conversation_urn = result["conversation_urn"]
                print("✅ Resolved URNs via name/URL lookup!")
                print(f"   Mailbox URN: {mailbox_urn}")
                print(f"   Conversation URN: {conversation_urn}")
            else:
                print("❌ No existing conversation found for that name/URL.")
                
                # Check if person might exist but no conversation yet
                person_exists = extractor.check_if_person_exists(input_value)
                
                print()
                if person_exists:
                    print("✅ Profile appears to be valid, but you haven't messaged them yet.")
                    print()
                    print("💡 LinkedIn API Limitation:")
                    print("   • You can only send messages to people you've ALREADY messaged before")
                    print("   • LinkedIn doesn't allow creating new conversations via API")
                    print()
                    print("🔧 To message this person:")
                    print(f"   1. Go to: {input_value}")
                    print("   2. Click 'Message' button on their profile")
                    print("   3. Send at least one message manually")
                    print("   4. Then come back and use this script for automated messaging")
                else:
                    print("❓ Could not verify if this profile exists.")
                    print()
                    print("💡 Possible reasons:")
                    print("   • Person is not in your network")
                    print("   • Invalid profile URL or name")
                    print("   • You haven't messaged them before")
                    print()
                    print("🔧 To fix this:")
                    print("   1. Go to LinkedIn.com and search for the person")
                    print("   2. Make sure you can find their profile")
                    print("   3. Send them a connection request first (if needed)")
                    print("   4. Send at least one message manually")
                    print("   5. Then use this script for automated messaging")
                
                print()
                print("⚠️  This is a LinkedIn security feature to prevent spam.")
                exit(1)
        except Exception as e:
            print(f"❌ Error during name/URL lookup: {e}")
            exit(1)
    else:
        print("❌ No name or URL provided. Please enter a recipient's name or LinkedIn profile URL.")
        exit(1)

    # Send message directly using the (possibly updated) URNs
    if mailbox_urn and conversation_urn:
        # Create payload dynamically with extracted URNs
        payload = {
            "message": {
                "body": {
                    "attributes": [],
                    "text": "Hi "
                },
                "renderContentUnions": [],
                "conversationUrn": conversation_urn,
                "originToken": str(uuid.uuid4())  # Generate unique origin token
            },
            "mailboxUrn": mailbox_urn,
            "trackingId": str(uuid.uuid4())[:16],  # Generate unique tracking ID
            "dedupeByClientGeneratedToken": False
        }
        
        url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage"
        
        print(f"📤 Sending message…")
        print(f"🎯 To: {mailbox_urn}")
        print(f"💬 Conversation: {conversation_urn}")
        
        response = session.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            print("🎉 SUCCESS! Message sent with automated URN extraction!")
            try:
                print(f"✅ Response: {response.json()}")
            except Exception:
                # Response might not be JSON
                print("✅ Message sent (non-JSON response).")
        else:
            print(f"❌ Failed to send message. Status: {response.status_code}")
            print(f"Response: {response.text}")
    else:
        print("😞 Could not send message – missing URNs")

