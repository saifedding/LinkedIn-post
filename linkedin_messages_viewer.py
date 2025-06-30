#!/usr/bin/env python3
"""
LinkedIn Messages Viewer
Shows all messages between you and a specific person by name
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import quote
from linkedin_conversation_extractor import LinkedInConversationExtractor

class LinkedInMessagesViewer:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.extractor = LinkedInConversationExtractor()
        
    def setup_session(self):
        """Setup session with cookies and headers from PowerShell script"""
        
        # Updated cookies from your PowerShell script
        cookies = {
            "bcookie": "v=2&12e9e7e4-3797-4b9d-8b85-e67c6fbbcf80",
            "li_sugr": "9c83b1f7-b3ab-47d6-8f9c-aac27e761ba1",
            "bscookie": "v=1&20250507140639ea67aaf7-6f73-48ff-8813-9f6383cea24eAQEBEVVX01KNZ7vWOUKdmFDVKvhshdNt",
            "JSESSIONID": "ajax:4763283604314235653",
            "_guid": "c4c27323-6441-4b94-8a60-e2dae58ecd41",
            "dfpfpt": "3c04e81e591e469e8cf3481efad5f950",
            "timezone": "Asia/Dubai",
            "li_theme": "light",
            "li_theme_set": "app",
            "lang": "v=2&lang=en-us",
            "sdui_ver": "sdui-flagship:0.1.7528+sdui-flagship.production",
            "AnalyticsSyncHistory": "AQK_eRy5LiZXJwAAAZe_qwIzZO_LbAvR1FcGJx_R_9rnkDNCrWvjKOrN4xZRuE9zGUzaO0h_W6fvC-YYrXQ8_g",
            "lms_ads": "AQFoZ9eixF7W9QAAAZe_qwNjC795bG516Cjoay0Fp4cps3lqbp22VjVaACbyOztnJzCZ6lCz7HhEPJ3UOOWXqkL1SFU_gjmk",
            "lms_analytics": "AQFoZ9eixF7W9QAAAZe_qwNjC795bG516Cjoay0Fp4cps3lqbp22VjVaACbyOztnJzCZ6lCz7HhEPJ3UOOWXqkL1SFU_gjmk",
            "fptctx2": "taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO1OZsqBMQoiv4L3v0T63VjmZLQa16kvaMUYVUosFXHHtS3l3aC7%2bp1EFIAkHKyNtQRBhoos8j9BfdkViImt83dvAFqcppQGcz5heoO6EHiT%2f2WMpn0HnQ95d0aiXGAk8qxAFHAMLZtFLr%2blIlevK84W1%2b%2bkBdGvNOFAGbYVWU9%2bRQrmV1NCHYTbXWOVIMufooVyvn%2b2lWgJdSY0VV9at63Pp9oekq7qQy4YLLD0O7%2blXCahZrDDNixWQiWnqhEunmFk2yWWGzorslBwL41%2fpFSaILdUYnycPsPgWuVPqOAFnuNVzPw7iXHOHljjkisgY7M%3d",
            "AMCVS_14215E3D5995C57C0A495C55@AdobeOrg": "1",
            "AMCV_14215E3D5995C57C0A495C55@AdobeOrg": "-637568504|MCIDTS|20270|MCMID|27573806750435840703114589459359274076|MCOPTOUT-1751285608s|NONE|vVersion|5.1.1",
            "g_state": '{"i_l":0}',
            "liap": "true",
            "li_at": "AQEDASP6v4EBfhJ7AAABl8BT3OQAAAGX5GBg5E0AocvtLBfU2unQg6KLYHNi6AG83PSJwqQdkZ2kcjhYnS0jlwh0Xy834jLziuj_Kdg3yOwz-L-QrbzlBOjMqHho03KrmOqhKNRdfYXUPajAOyj_oUg_",
            "UserMatchHistory": "AQKiB7Llh0h5CQAAAZfAzXrmCXAhnShmdUN0FvF8Es2ZeNaRCmct8q0-S1Ddqopi_SycvSKRb49MiK9AS3cJKZrwp_sa8bRYUrSwYtHjWey1gs7IdGFey4EkhbDn-gacF7IVWHbEq853dlv3k51Xg_QnSRDWZj7W8OWyQEAkzh5Opv9FX2epXGZQl0CmkaVhpnBrf9h6MwAGmxFlkXANNJ3CKSTBv61DQw87g5a_Cm86FS_GsBO9c7shNBmraSgxD-C3jxl8gBJ8UECnagqMbKfEknF3ZM5LBATJhV6LPTDiqSmaQc0nX1jE63pH3OPqgPYWcHzhBak1uE2Hl8Dvbhc-i9A9ZO7k87B_IBjYsd-47qITiw",
            "lidc": "b=OGST08:s=O:r=O:a=O:p=O:g=3239:u=1:x=1:i=1751286381:t=1751372781:v=2:sig=AQFU3gS41--2hDPcPVRLGY0B5NNnW-3M"
        }
        
        # Set cookies in session
        self.session.cookies.update(cookies)
        
        # Set User-Agent
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        })

    def get_messages(self, conversation_urn: str) -> Optional[Dict]:
        """
        Get all messages from a specific conversation using GraphQL API
        
        Args:
            conversation_urn: The conversation URN to fetch messages from
            
        Returns:
            JSON response from LinkedIn messages API
        """
        
        try:
            # GraphQL endpoint and parameters from your PowerShell script
            base_url = "https://www.linkedin.com/voyager/api/voyagerMessagingGraphQL/graphql"
            query_id = "messengerMessages.455dde239612d966346c1d1c4352f648"
            
            # URL encode the conversation URN
            encoded_urn = quote(conversation_urn, safe='')
            variables = f"(conversationUrn:{encoded_urn})"
            
            # Complete URL
            url = f"{base_url}?queryId={query_id}&variables={variables}"
            
            print(f"🔍 Fetching messages from conversation...")
            print(f"📞 Conversation URN: {conversation_urn}")
            
            # Headers from PowerShell script
            headers = {
                "authority": "www.linkedin.com",
                "accept": "application/graphql",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.7",
                "csrf-token": "ajax:4763283604314235653",
                "priority": "u=1, i",
                "referer": f"https://www.linkedin.com/messaging/thread/{conversation_urn.split(',')[-1].rstrip(')')}/",
                "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "sec-gpc": "1",
                "x-li-lang": "en_US",
                "x-li-page-instance": "urn:li:page:d_flagship3_messaging_conversation_detail;QihFVZaoQ6+K0d4elfLkPw==",
                "x-li-track": '{"clientVersion":"1.13.36800.3","mpVersion":"1.13.36800.3","osName":"web","timezoneOffset":4,"timezone":"Asia/Dubai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2.5,"displayWidth":3600,"displayHeight":2250}',
                "x-restli-protocol-version": "2.0.0"
            }
            
            response = self.session.get(url, headers=headers)
            
            print(f"📈 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
            return None

    def extract_messages(self, api_response: Dict) -> List[Dict]:
        """
        Extract message data from LinkedIn messages API response
        
        Args:
            api_response: JSON response from LinkedIn messages API
            
        Returns:
            List of message data with text, sender, timestamp, etc.
        """
        messages = []
        
        try:
            # Navigate through the GraphQL response structure
            data = api_response.get('data', {})
            messaging_data = data.get('messengerMessagesBySyncToken', {})
            elements = messaging_data.get('elements', [])
            
            print(f"📊 Found {len(elements)} messages")
            
            for element in elements:
                message = {}
                
                # Get message text
                body = element.get('body', {})
                message_text = body.get('text', '') if body else ''
                message['text'] = message_text
                
                # Get timestamp
                delivered_at = element.get('deliveredAt', 0)
                message['timestamp'] = delivered_at
                message['datetime'] = datetime.fromtimestamp(delivered_at / 1000) if delivered_at else None
                
                # Get sender information
                sender = element.get('sender', {})
                participant_type = sender.get('participantType', {})
                member = participant_type.get('member', {})
                
                if member:
                    # Extract sender name
                    first_name_obj = member.get('firstName', {})
                    first_name = first_name_obj.get('text', '') if isinstance(first_name_obj, dict) else str(first_name_obj)
                    
                    last_name_obj = member.get('lastName', {})
                    last_name = last_name_obj.get('text', '') if isinstance(last_name_obj, dict) else str(last_name_obj)
                    
                    message['sender_name'] = f"{first_name} {last_name}".strip()
                    message['sender_first_name'] = first_name
                    message['sender_last_name'] = last_name
                    
                    # Extract sender URN
                    message['sender_urn'] = sender.get('hostIdentityUrn', '')
                else:
                    message['sender_name'] = 'Unknown'
                    message['sender_urn'] = sender.get('hostIdentityUrn', '')
                
                # Get message URN
                message['message_urn'] = element.get('entityUrn', '')
                message['backend_urn'] = element.get('backendUrn', '')
                
                messages.append(message)
                
        except Exception as e:
            print(f"❌ Error extracting message data: {e}")
            
        return messages

    def format_messages(self, messages: List[Dict], participant_name: str) -> str:
        """
        Format messages for display in chat format
        
        Args:
            messages: List of message data
            participant_name: Name of the person you're chatting with
            
        Returns:
            Formatted string of the conversation
        """
        if not messages:
            return "❌ No messages found in this conversation."
        
        # Sort messages by timestamp (oldest first)
        messages.sort(key=lambda x: x.get('timestamp', 0))
        
        # Your name (from first message)
        your_name = None
        for msg in messages:
            if 'SAIFEDDINE' in msg.get('sender_name', ''):
                your_name = msg['sender_name']
                break
        
        if not your_name:
            your_name = "You"
        
        formatted = []
        formatted.append("=" * 80)
        formatted.append(f"💬 CONVERSATION WITH {participant_name.upper()}")
        formatted.append("=" * 80)
        formatted.append(f"📊 Total Messages: {len(messages)}")
        
        if messages:
            first_msg = messages[0]
            last_msg = messages[-1]
            
            if first_msg.get('datetime'):
                formatted.append(f"📅 First Message: {first_msg['datetime'].strftime('%Y-%m-%d %H:%M:%S')}")
            if last_msg.get('datetime'):
                formatted.append(f"📅 Last Message: {last_msg['datetime'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        formatted.append("-" * 80)
        
        for i, msg in enumerate(messages, 1):
            sender = msg.get('sender_name', 'Unknown')
            text = msg.get('text', '').strip()
            timestamp = msg.get('datetime')
            
            if not text:
                continue  # Skip empty messages
            
            # Format timestamp
            time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'Unknown time'
            
            # Determine if it's you or the other person
            if 'SAIFEDDINE' in sender or sender == your_name:
                sender_display = "🟢 You"
            else:
                sender_display = f"🔵 {sender}"
            
            formatted.append(f"\n📱 Message {i} | {time_str}")
            formatted.append(f"{sender_display}: {text}")
        
        formatted.append("\n" + "=" * 80)
        
        return "\n".join(formatted)

    def view_messages_by_name(self, person_name: str) -> str:
        """
        Get and display all messages with a specific person by their name
        
        Args:
            person_name: Name of the person to view messages with
            
        Returns:
            Formatted conversation string
        """
        
        print(f"🔍 Looking up conversation with: '{person_name}'")
        print("-" * 50)
        
        # Step 1: Get the conversation URN for this person
        result = self.extractor.get_urns_by_name(person_name)
        
        if not result:
            return f"❌ No conversation found with '{person_name}'. Make sure you have an existing conversation with this person."
        
        conversation_urn = result['conversation_urn']
        full_name = result['full_name']
        
        print(f"✅ Found conversation with: {full_name}")
        print(f"📞 Conversation URN: {conversation_urn}")
        
        # Step 2: Get all messages from this conversation
        api_response = self.get_messages(conversation_urn)
        
        if not api_response:
            return f"❌ Failed to fetch messages from conversation with {full_name}"
        
        # Step 3: Extract and format messages
        messages = self.extract_messages(api_response)
        
        if not messages:
            return f"❌ No messages found in conversation with {full_name}"
        
        # Step 4: Format for display
        formatted_conversation = self.format_messages(messages, full_name)
        
        return formatted_conversation

def view_conversation(person_name: str):
    """
    Simple function to view conversation with a person
    
    Args:
        person_name: Name of the person to view messages with
    """
    viewer = LinkedInMessagesViewer()
    conversation = viewer.view_messages_by_name(person_name)
    print(conversation)
    return conversation

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line usage: python linkedin_messages_viewer.py "oussama"
        name = " ".join(sys.argv[1:])
        view_conversation(name)
    else:
        # Interactive usage
        viewer = LinkedInMessagesViewer()
        
        print("💬 LinkedIn Messages Viewer")
        print("=" * 50)
        
        while True:
            print("\nOptions:")
            print("1. View messages with a specific person")
            print("2. Exit")
            
            choice = input("\nChoose an option (1-2): ").strip()
            
            if choice == "1":
                name = input("Enter person's name: ").strip()
                if name:
                    print()
                    conversation = viewer.view_messages_by_name(name)
                    print(conversation)
                    
                    # Ask if they want to save to file
                    save = input("\n💾 Save conversation to file? (y/n): ").strip().lower()
                    if save == 'y':
                        filename = f"conversation_{name.replace(' ', '_').lower()}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(conversation)
                        print(f"✅ Conversation saved to: {filename}")
                else:
                    print("❌ Please enter a name")
                    
            elif choice == "2":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please choose 1-2.")
                
            input("\nPress Enter to continue...") 