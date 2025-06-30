#!/usr/bin/env python3
"""
LinkedIn Profile URN Extractor

This script extracts the profile URN (hostRecipientUrns) from a LinkedIn profile URL.
This is useful for messaging someone you've never messaged before.
"""

import requests
import re
import json
import html
from typing import Dict, Optional
import sys
import uuid

class LinkedInProfileURNExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session with cookies and headers from script"""
        
        # Updated cookies from PowerShell script
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
            "fptctx2": "taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO1OZsqBMQoiv4L3v0T63VjmZLQa16kvaMUYVUosFXHHtS3l3aC7%252bp1EFIAkHKyNtQRBhoos8j9BfdkViImt83dvAFqcppQGcz5heoO6EHiT%252f2WMpn0HnQ95d0aiXGAk8qxAFHAMLZtFLr%252blIlevK84W1%252b%252bkBdGvNOFAGbYVWU9%252bRQrmV1NCHYTbXWOVIMufooVyvn%252b2lWgJdSY0VV9at63Pp9oekq7qQy4YLLD0O7%252blXCahZrDDNixWQiWnqhEunmFk2yWWGzorslBwL41%252fpFSaILdUYnycPsPgWuVPqOAFnuNVzPw7iXHOHljjkisgY7M%253d",
            "AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg": "1",
            "AMCV_14215E3D5995C57C0A495C55%40AdobeOrg": "-637568504%7CMCIDTS%7C20270%7CMCMID%7C27573806750435840703114589459359274076%7CMCOPTOUT-1751285608s%7CNONE%7CvVersion%7C5.1.1",
            "g_state": '{"i_l":0}',
            "liap": "true",
            "li_at": "AQEDASP6v4EBfhJ7AAABl8BT3OQAAAGX5GBg5E0AocvtLBfU2unQg6KLYHNi6AG83PSJwqQdkZ2kcjhYnS0jlwh0Xy834jLziuj_Kdg3yOwz-L-QrbzlBOjMqHho03KrmOqhKNRdfYXUPajAOyj_oUg_",
            "UserMatchHistory": "AQIopFDFe5LoIwAAAZfBXhApKuszIAJZaXyTcOyZXQdY12yUWz18W0E-pj5F2LJfj9w-GwjhOtHH89ymxGphxiJGi_Kc_ArWucsmtND9hvPSfUwEXF_izt_JYMuTE2QZYx2T2f_bIG_VjX7lJV2EGyixr7vCY7JkHfMylkO5PAyuxL2Chep7GhpJP5ocXNXnls0exgVhn8g2uzxs9eHGc2yLIxaTiqh_q_DfFIyekEjPzGrE7Htey--cyh2Xkzq01RRJWqohQrGMrpHO_PbVN5ItuyU6xEIS3n15tAL5ZoJRnAmJ5T0hYw_redRrD34bYewRR6RrsJTZv_UAqNnnD2VELr97P8tZDMOd5wQM7Fbz8ClCLQ",
            "lidc": 'b=VB85:s=V:r=V:a=V:p=V:g=5950:u=788:x=1:i=1751295857:t=1751377341:v=2:sig=AQF0M2-1z0rTjk9jqZtQFPrF42H7id2O',
        }
        
        # Set cookies in session
        self.session.cookies.update(cookies)
        
        # Set User-Agent and other headers
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "csrf-token": "ajax:4763283604314235653",
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-li-lang": "en_US",
            "x-restli-protocol-version": "2.0.0"
        })

    def clean_urn(self, urn: str) -> str:
        """Clean URN by removing HTML entities and unwanted characters"""
        if not urn:
            return urn
        
        # Remove HTML entities
        urn = html.unescape(urn)
        
        # Remove quotes and other unwanted characters at the end
        urn = re.sub(r'["\'\s&;]+$', '', urn)
        
        return urn

    def get_public_identifier_from_url(self, profile_url: str) -> Optional[str]:
        """Extract public identifier from LinkedIn profile URL"""
        try:
            if '/in/' in profile_url:
                # Extract everything after '/in/' and remove trailing slash
                public_id = profile_url.split('/in/')[-1].strip('/')
                # Remove any query parameters or fragments
                public_id = public_id.split('?')[0].split('#')[0]
                return public_id
        except Exception as e:
            print(f"❌ Error extracting public ID from URL: {e}")
        return None

    def extract_profile_urn_from_url(self, profile_url: str) -> Optional[str]:
        """Extract LinkedIn profile URN from profile URL"""
        try:
            print(f"🔍 Extracting URN from profile: {profile_url}")
            
            # If already a URN, clean and return it
            if profile_url.startswith('urn:li:fsd_profile:'):
                return self.clean_urn(profile_url)
            
            # Normalize URL if needed
            if not profile_url.startswith('http'):
                public_id = self.get_public_identifier_from_url(profile_url)
                if public_id:
                    profile_url = f"https://www.linkedin.com/in/{public_id}/"
                else:
                    profile_url = f"https://www.linkedin.com/in/{profile_url}/"
            
            # First, let's try the voyager API for more reliable extraction
            public_id = self.get_public_identifier_from_url(profile_url)
            if public_id:
                urn = self.get_profile_urn_from_public_id(public_id)
                if urn:
                    return urn
            
            # Fallback method: Try to extract URN from page source
            profile_headers = self.session.headers.copy()
            profile_headers.update({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'referer': 'https://www.linkedin.com/',
                'x-li-page-instance': f"urn:li:page:d_flagship3_profile_view_base;{uuid.uuid4()}",
            })
            
            response = self.session.get(profile_url, headers=profile_headers)
            
            if response.status_code == 200:
                # Look for profile URN in the page source with multiple patterns
                urn_patterns = [
                    # Specifically target patterns that look for OTHER profiles, not your own
                    r'urn:li:fsd_profile:([A-Za-z0-9_-]{16,24})',  # Basic pattern
                    r'"miniProfile":"urn:li:fs_miniProfile:([^"]+)"',
                    r'"profileUrn":"urn:li:fsd_profile:([^"]+)"',
                    r'&quot;profileUrn&quot;:&quot;urn:li:fsd_profile:([^&]+)&quot;',
                    r'"urn:li:fsd_profile:([^"]+)"'
                ]
                
                all_urns = []
                your_urn = "ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc"  # Your own URN to filter out
                
                for pattern in urn_patterns:
                    matches = re.findall(pattern, response.text)
                    for match in matches:
                        # Clean up the match
                        if match and match != your_urn and "ACoAA" in match:
                            all_urns.append(match)
                
                # Filter out duplicates and your own URN
                unique_urns = [u for u in set(all_urns) if your_urn not in u]
                
                if unique_urns:
                    # Use the first URN that's not yours
                    urn_id = unique_urns[0]
                    full_urn = f"urn:li:fsd_profile:{urn_id}"
                    cleaned_urn = self.clean_urn(full_urn)
                    print(f"✅ Found URN: {cleaned_urn}")
                    return cleaned_urn
                
                print(f"⚠️ Found {len(all_urns)} URNs but couldn't find one matching the profile")
                
                # Try direct API method as a last resort
                print("🔄 Trying direct API lookup...")
                member_urn = self.get_member_urn_from_page(response.text, profile_url)
                if member_urn:
                    return member_urn
            else:
                print(f"❌ Failed to access profile. Status code: {response.status_code}")
            
            return None
            
        except Exception as e:
            print(f"❌ Error extracting profile URN: {e}")
            return None
    
    def get_member_urn_from_page(self, page_content: str, profile_url: str) -> Optional[str]:
        """Extract member URN from page content using various methods"""
        try:
            # Look for entityUrn in various formats
            entity_patterns = [
                r'"memberEntityUrn":"([^"]+)"',
                r'"entityUrn":"([^"]+)"',
                r'entityUrn=([^&]+)',
                r'"urn:li:member:([^"]+)"'
            ]
            
            for pattern in entity_patterns:
                matches = re.findall(pattern, page_content)
                if matches:
                    for entity_urn in matches:
                        if ":" in entity_urn and "fsd_profile:" in entity_urn:
                            return self.clean_urn(entity_urn)
                        elif entity_urn.isdigit() or entity_urn.startswith("ACoAA"):
                            return f"urn:li:fsd_profile:{entity_urn}"
            
            # Try to find member ID in meta tags or specific divs
            member_id_patterns = [
                r'data-member-id="(\d+)"',
                r'data-profileid="(\d+)"',
                r'member-id=(\d+)',
                r'memberId=(\d+)',
                r'fs_miniProfile:(\w+)'
            ]
            
            for pattern in member_id_patterns:
                matches = re.findall(pattern, page_content)
                if matches:
                    member_id = matches[0]
                    if member_id.isdigit() or member_id.startswith("ACoAA"):
                        return f"urn:li:fsd_profile:{member_id}"
            
            # Try extracting from image URLs which often contain profile IDs
            img_patterns = [
                r'profile-displayphoto-shrink_\d+_\d+/\d+/\d+/\d+/([^/]+)/',
                r'media-exp\d+-\d+\.licdn\.com/dms/image/[^/]+/profile-displayphoto-shrink_\d+_\d+/\d+/\d+/\d+/([^/\?]+)'
            ]
            
            for pattern in img_patterns:
                matches = re.findall(pattern, page_content)
                if matches:
                    for img_id in matches:
                        if img_id != "person-placeholder" and len(img_id) > 8:
                            return f"urn:li:fsd_profile:{img_id}"
            
            return None
            
        except Exception as e:
            print(f"❌ Error extracting member URN: {e}")
            return None

    def get_profile_urn_from_public_id(self, public_id: str) -> Optional[str]:
        """Get profile URN using the public identifier via voyager API"""
        try:
            print(f"🔍 Looking up URN for public ID: {public_id}")
            
            # Use the voyager identity API
            url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}"
            
            headers = self.session.headers.copy()
            headers.update({
                "accept": "application/vnd.linkedin.normalized+json+2.1",
                "referer": f"https://www.linkedin.com/in/{public_id}/",
                "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{uuid.uuid4()}",
                "x-restli-protocol-version": "2.0.0",
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Extract profile URN from the response
                    entity_urn = None
                    
                    # Look in included elements for profile URNs
                    if 'included' in data:
                        for element in data['included']:
                            if 'entityUrn' in element:
                                urn = element['entityUrn']
                                if 'fsd_profile' in urn:
                                    urn_id = urn.split(':')[-1]
                                    if urn_id.startswith("ACoAA") and "CP6v4" not in urn_id:  # Skip your own URN
                                        entity_urn = urn
                                        break
                    
                    # Check main object if not found in included
                    if not entity_urn and 'entityUrn' in data:
                        entity_urn = data['entityUrn']
                    
                    # Check for miniProfile with publicIdentifier match
                    if not entity_urn and 'included' in data:
                        your_urn = "ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc"  # Your URN to exclude
                        for element in data['included']:
                            if 'publicIdentifier' in element and element.get('publicIdentifier') == public_id:
                                if 'entityUrn' in element:
                                    urn = element['entityUrn']
                                    urn_id = urn.split(':')[-1] if ':' in urn else urn
                                    if urn_id != your_urn:
                                        entity_urn = urn
                                        break
                    
                    if entity_urn and 'fsd_profile' in entity_urn:
                        cleaned_urn = self.clean_urn(entity_urn)
                        print(f"✅ Found URN via API: {cleaned_urn}")
                        return cleaned_urn
                    
                    # Backup method: Search through entire response for URNs
                    response_text = json.dumps(data)
                    urn_patterns = [
                        r'urn:li:fsd_profile:([A-Za-z0-9_-]{16,24})',
                        r'"miniProfile":"urn:li:fs_miniProfile:([^"]+)"'
                    ]
                    
                    all_urns = []
                    for pattern in urn_patterns:
                        matches = re.findall(pattern, response_text)
                        all_urns.extend(matches)
                    
                    # Filter out your own URN
                    your_urn = "ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc"  # Your URN to exclude
                    unique_urns = [u for u in set(all_urns) if your_urn not in u and u.startswith("ACoAA")]
                    
                    if unique_urns:
                        urn_id = unique_urns[0]
                        full_urn = f"urn:li:fsd_profile:{urn_id}"
                        cleaned_urn = self.clean_urn(full_urn)
                        print(f"✅ Found URN in API response: {cleaned_urn}")
                        return cleaned_urn
                except json.JSONDecodeError:
                    print("❌ Failed to parse API response as JSON")
                    
                    # Try to extract URN directly from response text
                    urn_patterns = [
                        r'"publicIdentifier":"' + re.escape(public_id) + r'[^}]+"objectUrn":"([^"]+)"',
                        r'"urn:li:fsd_profile:([A-Za-z0-9_-]{16,24})"'
                    ]
                    
                    for pattern in urn_patterns:
                        matches = re.findall(pattern, response.text)
                        if matches:
                            for match in matches:
                                if match != "ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc":  # Skip your own URN
                                    full_urn = f"urn:li:fsd_profile:{match}"
                                    if not full_urn.startswith("urn:li:"):
                                        full_urn = f"urn:li:fsd_profile:{match}"
                                    cleaned_urn = self.clean_urn(full_urn)
                                    print(f"✅ Found URN via text parsing: {cleaned_urn}")
                                    return cleaned_urn
            else:
                print(f"❌ API request failed. Status code: {response.status_code}")
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting profile URN from public ID: {e}")
            return None

    def get_messaging_urns(self, profile_url: str) -> Dict:
        """
        Get messaging URNs for a profile URL
        
        Returns:
            Dict with mailbox_urn, hostRecipientUrns, and your_urn
        """
        result = {}
        
        # Your own URN (sender)
        your_urn = "urn:li:fsd_profile:ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc"
        result["your_urn"] = your_urn
        result["mailbox_urn"] = your_urn
        
        # Extract recipient's URN from profile URL
        recipient_urn = self.extract_profile_urn_from_url(profile_url)
        
        if recipient_urn:
            # For LinkedIn's API format, we need just the ID part after the last colon
            if ":" in recipient_urn:
                recipient_id = recipient_urn.split(":")[-1]
                result["hostRecipientUrns"] = [f"urn:li:fsd_profile:{recipient_id}"]
                result["recipient_urn"] = f"urn:li:fsd_profile:{recipient_id}"
                
                # Format for the payload
                result["formatted_payload"] = {
                    "message": {
                        "body": {
                            "attributes": [],
                            "text": "YOUR_MESSAGE_HERE"
                        },
                        "originToken": str(uuid.uuid4()),
                        "renderContentUnions": []
                    },
                    "mailboxUrn": your_urn,
                    "trackingId": str(uuid.uuid4())[:16],
                    "dedupeByClientGeneratedToken": False,
                    "hostRecipientUrns": [f"urn:li:fsd_profile:{recipient_id}"]
                }
                
                # PowerShell style JSON for easy copy-paste
                ps_json = json.dumps(result["formatted_payload"]).replace('"', '`"')
                result["powershell_json"] = ps_json
        
        return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_profile_urns.py <linkedin_profile_url>")
        print("Example: python get_profile_urns.py https://www.linkedin.com/in/johndoe/")
        sys.exit(1)
    
    profile_url = sys.argv[1]
    extractor = LinkedInProfileURNExtractor()
    result = extractor.get_messaging_urns(profile_url)
    
    if "hostRecipientUrns" in result:
        print("\n" + "="*80)
        print("✅ LINKEDIN PROFILE URN EXTRACTION SUCCESSFUL")
        print("="*80)
        print(f"🔹 Your URN (mailbox_urn): {result['your_urn']}")
        print(f"🔹 Recipient URN (hostRecipientUrns): {result['hostRecipientUrns'][0]}")
        
        print("\n" + "="*80)
        print("📝 READY-TO-USE JSON FOR API REQUEST")
        print("="*80)
        print(json.dumps(result["formatted_payload"], indent=2))
        
        print("\n" + "="*80)
        print("🔧 POWERSHELL EXAMPLE")
        print("="*80)
        print("$body = " + result["powershell_json"])
        
        print("\n💡 Replace 'YOUR_MESSAGE_HERE' with your actual message text")
    else:
        print("\n❌ Failed to extract URNs from profile")
        print("Try one of these solutions:")
        print("1. Make sure you're logged into LinkedIn")
        print("2. Check if the profile URL is correct")
        print("3. Try with a different profile")

if __name__ == "__main__":
    main() 