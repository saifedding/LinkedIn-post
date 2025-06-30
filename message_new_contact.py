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
        
        # Add required headers for messaging
        self.session.headers.update({
            "content-type": "text/plain;charset=UTF-8",
            "origin": "https://www.linkedin.com"
        })
        
    def extract_urns(self, profile_url: str) -> Dict:
        """Extract URNs from profile URL"""
        print(f"🔍 Extracting URNs from: {profile_url}")
        return self.extractor.get_messaging_urns(profile_url)
    
    def send_message(self, urns: Dict, message_text: str) -> bool:
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
        
        # API endpoint
        url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage"
        
        try:
            print(f"📤 Sending message to: {urns['recipient_urn']}")
            response = self.session.post(url, data=json.dumps(payload))
            
            if response.status_code == 200:
                print("✅ Message sent successfully!")
                return True
            else:
                print(f"❌ Failed to send message. Status: {response.status_code}")
                print(f"Response: {response.text[:200]}")
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
    success = messenger.send_message(urns, message_text)
    
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