#!/usr/bin/env python3
"""
LinkedIn Message New Contact

This script combines the profile URN extractor and message sender to send
messages to LinkedIn contacts you've never messaged before.
"""

import sys
import json
import requests
import uuid
from typing import Dict, Optional
from get_profile_urns import LinkedInProfileURNExtractor

class NewContactMessenger:
    def __init__(self):
        self.extractor = LinkedInProfileURNExtractor()
        self.session = requests.Session()
        self.session.cookies = self.extractor.session.cookies
        self.session.headers = self.extractor.session.headers.copy()
        
        # Add required headers for messaging (matching PowerShell script)
        self.session.headers.update({
            "authority": "www.linkedin.com",
            "method": "POST",
            "path": "/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage",
            "scheme": "https",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://www.linkedin.com",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-li-lang": "en_US",
            "x-li-track": '{"clientVersion":"1.13.36800.3","mpVersion":"1.13.36800.3","osName":"web","timezoneOffset":4,"timezone":"Asia/Dubai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2.5,"displayWidth":3840,"displayHeight":2400}',
            "content-type": "text/plain;charset=UTF-8"
        })
        
    def extract_urns(self, profile_url: str) -> Dict:
        """Extract URNs from profile URL"""
        print(f"🔍 Extracting URNs from: {profile_url}")
        return self.extractor.get_messaging_urns(profile_url)
    
    def send_message(self, urns: Dict, message_text: str, profile_url: str) -> bool:
        """Send a message using extracted URNs"""
        if not urns or "hostRecipientUrns" not in urns:
            print("❌ Missing required URNs for messaging")
            return False
        
        # Prepare message payload
        payload = urns["formatted_payload"]
        payload["message"]["body"]["text"] = message_text
        
        # Update tokens to be fresh
        payload["originToken"] = str(uuid.uuid4())
        payload["trackingId"] = str(uuid.uuid4())[:16]
        
        # Update headers with specific referer and page instance for this profile
        headers = self.session.headers.copy()
        headers.update({
            "referer": profile_url,
            "x-li-page-instance": "urn:li:page:d_flagship3_profile_view_base;hOn+xkrURFiK118ise1SZw=="
        })
        
        # API endpoint
        url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage"
        
        try:
            print(f"📤 Sending message to: {urns['recipient_urn']}")
            print(f"📄 Message: \"{message_text}\"")
            
            # Encode the payload exactly like PowerShell does
            json_body = json.dumps(payload, separators=(',', ':'))
            encoded_body = json_body.encode('utf-8')
            
            response = self.session.post(url, headers=headers, data=encoded_body)
            
            if response.status_code == 200:
                print("✅ Message sent successfully!")
                try:
                    response_data = response.json()
                    print(f"📋 Response: {response_data}")
                except:
                    print("📋 Response received (non-JSON)")
                return True
            else:
                print(f"❌ Failed to send message. Status: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return False
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

def main():
    # Show usage info if no args
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python message_new_contact.py <linkedin_profile_url> [message_text]")
        print("\nExample:")
        print("  python message_new_contact.py https://www.linkedin.com/in/johndoe/ 'Hello John, nice to connect!'")
        print("\nIf message_text is not provided, you'll be prompted to enter it.")
        sys.exit(1)
    
    # Extract profile URL and message
    profile_url = sys.argv[1]
    
    # Get message text from args or prompt
    if len(sys.argv) >= 3:
        message_text = sys.argv[2]
    else:
        message_text = input("Enter your message: ").strip()
        
    if not message_text:
        print("❌ Message text cannot be empty")
        sys.exit(1)
    
    # Initialize the messenger
    messenger = NewContactMessenger()
    
    # Extract URNs
    print("\n" + "="*80)
    print("STEP 1: EXTRACTING PROFILE URN")
    print("="*80)
    urns = messenger.extract_urns(profile_url)
    
    if not urns or "hostRecipientUrns" not in urns:
        print("\n❌ Failed to extract URNs from profile")
        print("This could be due to:")
        print("1. Invalid LinkedIn URL")
        print("2. Profile not accessible (private or requires login)")
        print("3. LinkedIn authentication cookies need to be updated")
        sys.exit(1)
        
    # Show the extracted URNs
    print("\n✅ Successfully extracted URNs:")
    print(f"Your URN: {urns['your_urn']}")
    print(f"Recipient URN: {urns['recipient_urn']}")
    
    # Confirm before sending
    print("\n" + "="*80)
    print("STEP 2: SENDING MESSAGE")
    print("="*80)
    print(f"Message to send: \"{message_text}\"")
    
    confirm = input("\nSend this message? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Message sending cancelled")
        sys.exit(0)
        
    # Send the message
    success = messenger.send_message(urns, message_text, profile_url)
    
    if success:
        print("\n" + "="*80)
        print("✅ SUCCESS: MESSAGE SENT")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("❌ ERROR: MESSAGE FAILED TO SEND")
        print("="*80)
        print("\nPossible reasons:")
        print("1. You can't message this person (they don't accept messages)")
        print("2. LinkedIn API limitations (new contacts may require a manual first message)")
        print("3. Authentication cookies expired")

if __name__ == "__main__":
    main() 