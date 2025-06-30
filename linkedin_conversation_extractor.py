#!/usr/bin/env python3
"""
LinkedIn Conversation Extractor
Converts PowerShell API call to Python and extracts conversation URNs with name mapping
"""

import requests
import json
import re
from typing import Dict, List, Optional
from urllib.parse import unquote

class LinkedInConversationExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
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
            "UserMatchHistory": "AQL952eah0yO1AAAAZfAf9ErXs9clfIaj4p_9O-EDIFvc9FTn07iQmplQcIggzP4oed3hB2u6qsGEpNjkWEglV-l6J0PryQSpFSGQ4qc1sEBEKRLo0JylLt5JgxGfkDmtqboWW2jQ7O8IR2L7EwzKSm-uI_Btw9wjtCUyER0D_SNZqWdybzLFnCBhF6eCP4hYO5X_5TvwkLDbRMuQxLxeNfPyXwmgouqF2TSxbmCbievRu6LDYiKCVh9JKPuNV9Y51agNEshKYNvq5GXwYXyGKCzNVlzX6lTRNXoed8FBC2uqMln5G6wc_UYURRjiENgAYCbw94TUuySeDKmTEhLM1pzCgK1QCX46H4ekkBOK8z_t5s67g",
            "lidc": "b=VB85:s=V:r=V:a=V:p=V:g=5950:u=786:x=1:i=1751281293:t=1751364351:v=2:sig=AQEPC_Arm-2jtVZwbPC2G1qP4qzCtncR"
        }
        
        # Set cookies in session
        self.session.cookies.update(cookies)
        
        # Set User-Agent
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        })

    def get_conversations(self, mailbox_urn: str = None, count: int = 20) -> Optional[Dict]:
        """
        Get LinkedIn conversations using GraphQL API
        
        Args:
            mailbox_urn: Your mailbox URN (if None, uses default from PowerShell)
            count: Number of conversations to fetch
            
        Returns:
            JSON response from LinkedIn API
        """
        
        # Default mailbox URN from your PowerShell script
        if not mailbox_urn:
            mailbox_urn = "urn:li:fsd_profile:ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc"
        
        # GraphQL endpoint and parameters from your PowerShell script
        base_url = "https://www.linkedin.com/voyager/api/voyagerMessagingGraphQL/graphql"
        query_id = "messengerConversations.45338e053010d1c19147f92de6de3ae6"
        
        # Build variables parameter
        variables = f"(query:(predicateUnions:List((conversationCategoryPredicate:(category:INBOX)))),count:{count},mailboxUrn:{mailbox_urn.replace(':', '%3A')},lastUpdatedBefore:1749318066019)"
        
        # Complete URL
        url = f"{base_url}?queryId={query_id}&variables={variables}"
        
        # Headers from PowerShell script
        headers = {
            "authority": "www.linkedin.com",
            "accept": "application/graphql",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.7",
            "csrf-token": "ajax:4763283604314235653",
            "priority": "u=1, i",
            "referer": "https://www.linkedin.com/messaging/thread/2-OTFiMjZmY2EtYzEwMC00MjE4LWEyNTMtY2YwNjM1YjVmZDkzXzAxMg==/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-li-lang": "en_US",
            "x-li-page-instance": "urn:li:page:d_flagship3_messaging_conversation_detail;soDQAIh6R7aUW+W297PyRQ==",
            "x-li-track": '{"clientVersion":"1.13.36800.3","mpVersion":"1.13.36800.3","osName":"web","timezoneOffset":4,"timezone":"Asia/Dubai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2.5,"displayWidth":3600,"displayHeight":2250}',
            "x-restli-protocol-version": "2.0.0"
        }
        
        try:
            print(f"🔍 Fetching conversations from LinkedIn...")
            print(f"📧 Mailbox URN: {mailbox_urn}")
            print(f"📊 Count: {count}")
            
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

    def extract_conversation_data(self, api_response: Dict) -> List[Dict]:
        """
        Extract conversation data from LinkedIn API response
        
        Args:
            api_response: JSON response from LinkedIn conversations API
            
        Returns:
            List of conversation data with URNs and participant info
        """
        conversations = []
        
        try:
            # Navigate through the GraphQL response structure
            data = api_response.get('data', {})
            messaging_data = data.get('messengerConversationsByCategoryQuery', {})
            elements = messaging_data.get('elements', [])
            
            print(f"📊 Found {len(elements)} conversations")
            
            for element in elements:
                conversation = {}
                
                # Get conversation URN
                conversation_urn = element.get('entityUrn', '')
                if conversation_urn:
                    conversation['conversation_urn'] = conversation_urn
                
                # Get participants from conversationParticipants
                participants = element.get('conversationParticipants', [])
                conversation['participants'] = []
                
                for participant in participants:
                    participant_data = {
                        'host_identity_urn': participant.get('hostIdentityUrn', ''),
                        'entity_urn': participant.get('entityUrn', '')
                    }
                    
                    # Extract profile URN from hostIdentityUrn
                    host_identity_urn = participant.get('hostIdentityUrn', '')
                    if host_identity_urn and 'urn:li:fsd_profile:' in host_identity_urn:
                        participant_data['profile_urn'] = host_identity_urn
                    
                    # Extract name info from participantType.member
                    participant_type = participant.get('participantType', {})
                    member = participant_type.get('member', {})
                    
                    if member:
                        # Extract first name
                        first_name_obj = member.get('firstName', {})
                        first_name = first_name_obj.get('text', '') if isinstance(first_name_obj, dict) else str(first_name_obj)
                        participant_data['first_name'] = first_name
                        
                        # Extract last name  
                        last_name_obj = member.get('lastName', {})
                        last_name = last_name_obj.get('text', '') if isinstance(last_name_obj, dict) else str(last_name_obj)
                        participant_data['last_name'] = last_name
                        
                        # Full name
                        full_name = f"{first_name} {last_name}".strip()
                        participant_data['full_name'] = full_name
                        
                        # Extract headline
                        headline_obj = member.get('headline', {})
                        headline = headline_obj.get('text', '') if isinstance(headline_obj, dict) else str(headline_obj)
                        participant_data['headline'] = headline
                        
                        # Extract profile URL and try to get public identifier
                        profile_url = member.get('profileUrl', '')
                        participant_data['profile_url'] = profile_url
                        
                        # Try to extract public identifier from profile URL
                        if profile_url and '/in/' in profile_url:
                            public_id = profile_url.split('/in/')[-1].strip('/')
                            participant_data['public_identifier'] = public_id
                        else:
                            participant_data['public_identifier'] = ''
                    
                    conversation['participants'].append(participant_data)
                
                # Get last activity and other metadata
                conversation['last_activity'] = element.get('lastActivityAt', 0)
                conversation['unread_count'] = element.get('unreadCount', 0)
                conversation['backend_urn'] = element.get('backendUrn', '')
                conversation['conversation_url'] = element.get('conversationUrl', '')
                
                conversations.append(conversation)
                
        except Exception as e:
            print(f"❌ Error extracting conversation data: {e}")
            
        return conversations

    def create_name_mapping(self, conversations: List[Dict]) -> Dict[str, Dict]:
        """
        Create a mapping from names to URNs
        
        Args:
            conversations: List of conversation data
            
        Returns:
            Dictionary mapping names to mailbox_urn and conversation_urn
        """
        name_mapping = {}
        
        # Your own URN (sender) - extract from default mailbox URN
        your_urn = "urn:li:fsd_profile:ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc"  # This should be YOUR URN
        
        for conv in conversations:
            conversation_urn = conv.get('conversation_urn', '')
            
            for participant in conv.get('participants', []):
                profile_urn = participant.get('profile_urn', '')
                full_name = participant.get('full_name', '')
                first_name = participant.get('first_name', '').lower()
                public_id = participant.get('public_identifier', '')
                
                # Skip if this is your own profile (don't map yourself)
                if profile_urn == your_urn:
                    continue
                
                if profile_urn and (full_name or first_name):
                    # Create multiple mappings for easier lookup
                    keys_to_map = []
                    
                    if first_name:
                        keys_to_map.append(first_name)
                    if full_name:
                        keys_to_map.append(full_name.lower())
                    if public_id:
                        keys_to_map.append(public_id.lower())
                    
                    mapping_data = {
                        'mailbox_urn': your_urn,  # YOUR URN (sender), not participant's URN
                        'conversation_urn': conversation_urn,
                        'recipient_urn': profile_urn,  # Add recipient URN for reference
                        'full_name': full_name,
                        'first_name': participant.get('first_name', ''),
                        'last_name': participant.get('last_name', ''),
                        'public_identifier': public_id,
                        'last_activity': conv.get('last_activity', 0),
                        'unread_count': conv.get('unread_count', 0)
                    }
                    
                    for key in keys_to_map:
                        if key:
                            name_mapping[key] = mapping_data
        
        return name_mapping

    def extract_public_id_from_url(self, profile_url: str) -> Optional[str]:
        """
        Extract public identifier from LinkedIn profile URL
        
        Args:
            profile_url: LinkedIn profile URL (e.g., https://www.linkedin.com/in/oussamagaham/)
            
        Returns:
            Public identifier (e.g., 'oussamagaham') or None if not found
        """
        try:
            if '/in/' in profile_url:
                # Extract everything after '/in/' and remove trailing slash
                public_id = profile_url.split('/in/')[-1].strip('/')
                # Remove any query parameters or fragments
                public_id = public_id.split('?')[0].split('#')[0]
                return public_id.lower()
        except Exception as e:
            print(f"❌ Error extracting public ID from URL: {e}")
        return None

    def check_if_person_exists(self, name_or_url: str) -> bool:
        """
        Check if a person exists in your LinkedIn network (even without conversation)
        This could be used to verify the person is findable before requiring manual first contact
        
        Args:
            name_or_url: Person's name or LinkedIn profile URL
            
        Returns:
            True if person seems to exist in network, False otherwise
        """
        # For now, this just checks if we can extract a valid public ID from URL
        # In future, could be enhanced to check LinkedIn search API
        
        if 'linkedin.com/in/' in name_or_url:
            public_id = self.extract_public_id_from_url(name_or_url)
            return public_id is not None and len(public_id) > 0
        
        # For names, we can't easily verify without existing conversation
        # This would require LinkedIn search API which has different limitations
        return False

    def get_urns_by_name(self, name_or_url: str) -> Optional[Dict]:
        """
        Get URNs for a specific person by name or LinkedIn profile URL
        
        Args:
            name_or_url: Person's name (first name, full name) or LinkedIn profile URL
            
        Returns:
            Dictionary with mailbox_urn and conversation_urn
        """
        # Get fresh conversation data
        api_response = self.get_conversations()
        if not api_response:
            return None
        
        # Extract conversations
        conversations = self.extract_conversation_data(api_response)
        
        # Create name mapping
        name_mapping = self.create_name_mapping(conversations)
        
        # Check if input is a LinkedIn URL
        if 'linkedin.com/in/' in name_or_url:
            print(f"🔗 Detected LinkedIn profile URL: {name_or_url}")
            public_id = self.extract_public_id_from_url(name_or_url)
            if public_id:
                print(f"🔍 Looking for public ID: {public_id}")
                # Look up by public identifier
                if public_id in name_mapping:
                    print(f"✅ Found by public ID: {public_id}")
                    return name_mapping[public_id]
                
                # Try partial matching for public ID
                for mapped_name, data in name_mapping.items():
                    if public_id in mapped_name or mapped_name in public_id:
                        print(f"✅ Found by partial public ID match: {mapped_name}")
                        return data
            
            print(f"❌ No conversation found for LinkedIn URL: {name_or_url}")
            return None
        
        # Otherwise treat as name lookup (existing functionality)
        name_lower = name_or_url.lower()
        print(f"👤 Looking for name: {name_lower}")
        
        if name_lower in name_mapping:
            print(f"✅ Found by exact name match: {name_lower}")
            return name_mapping[name_lower]
        
        # Try partial matching
        for mapped_name, data in name_mapping.items():
            if name_lower in mapped_name or mapped_name in name_lower:
                print(f"✅ Found by partial name match: {mapped_name}")
                return data
        
        print(f"❌ No conversation found for name: {name_or_url}")
        return None

    def print_all_conversations(self):
        """Print all conversations with participant details"""
        
        api_response = self.get_conversations()
        if not api_response:
            print("❌ Failed to get conversations")
            return
        
        conversations = self.extract_conversation_data(api_response)
        name_mapping = self.create_name_mapping(conversations)
        
        print("\n" + "="*80)
        print("📋 ALL LINKEDIN CONVERSATIONS")
        print("="*80)
        
        for i, conv in enumerate(conversations, 1):
            print(f"\n🔹 Conversation {i}:")
            print(f"   Conversation URN: {conv.get('conversation_urn', 'N/A')}")
            print(f"   Last Activity: {conv.get('last_activity', 'N/A')}")
            print(f"   Unread Count: {conv.get('unread_count', 0)}")
            
            print(f"   👥 Participants:")
            for participant in conv.get('participants', []):
                name = participant.get('full_name', 'Unknown')
                profile_urn = participant.get('profile_urn', 'N/A')
                public_id = participant.get('public_identifier', 'N/A')
                
                print(f"      - {name}")
                print(f"        Profile URN: {profile_urn}")
                print(f"        Public ID: {public_id}")
        
        print("\n" + "="*80)
        print("🔑 NAME TO URN MAPPING")
        print("="*80)
        
        for name, data in name_mapping.items():
            print(f"'{name}' -> Sender (Mailbox): {data['mailbox_urn']}")
            print(f"      -> Recipient: {data.get('recipient_urn', 'N/A')}")
            print(f"      -> Conversation: {data['conversation_urn']}")
            print()

# Quick helper functions
def get_urns_for_person(name_or_url: str) -> Optional[Dict]:
    """
    Simple function to get URNs for a person by name or LinkedIn profile URL
    
    Args:
        name_or_url: Person's name or LinkedIn profile URL
        
    Returns:
        Dict with mailbox_urn and conversation_urn or None
    """
    extractor = LinkedInConversationExtractor()
    return extractor.get_urns_by_name(name_or_url)

def quick_test():
    """Quick test to get URNs for Oussama"""
    print("🔍 Quick test for Oussama...")
    
    result = get_urns_for_person("oussama")
    if result:
        print("✅ Found Oussama's URNs:")
        print(f"mailbox_urn = \"{result['mailbox_urn']}\"")
        print(f"conversation_urn = \"{result['conversation_urn']}\"")
    else:
        print("❌ Oussama not found in conversations")

if __name__ == "__main__":
    # Test the extractor
    extractor = LinkedInConversationExtractor()
    
    print("🚀 LinkedIn Conversation Extractor")
    print("="*50)
    
    # Get all conversations
    print("\n📋 Getting all conversations...")
    extractor.print_all_conversations()
    
    # Test name lookup
    print("\n🔍 Testing name lookup for 'oussama'...")
    result = extractor.get_urns_by_name("oussama")
    
    if result:
        print("✅ Found:")
        print(f"   Mailbox URN: {result['mailbox_urn']}")
        print(f"   Conversation URN: {result['conversation_urn']}")
        print(f"   Full Name: {result['full_name']}")
    else:
        print("❌ Not found") 