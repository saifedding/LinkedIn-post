#!/usr/bin/env python3
"""
LinkedIn Connection Checker - Clean Version
Checks if a given LinkedIn profile is connected with you (without debug output)
"""

import requests
import json
import re
import sys
from typing import Dict, Optional
from urllib.parse import quote
import uuid

class LinkedInConnectionChecker:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session with cookies and headers"""
        
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
        
        self.session.cookies.update(cookies)
        
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "csrf-token": "ajax:4763283604314235653",
            "accept": "application/vnd.linkedin.normalized+json+2.1",
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

    def get_public_identifier_from_url(self, profile_url: str) -> Optional[str]:
        """Extract public identifier from LinkedIn profile URL"""
        try:
            if '/in/' in profile_url:
                public_id = profile_url.split('/in/')[-1].strip('/')
                public_id = public_id.split('?')[0].split('#')[0]
                return public_id
        except Exception:
            pass
        return None

    def extract_profile_name(self, data: Dict) -> Optional[str]:
        """Extract profile name from API response"""
        try:
            # Look for Profile and MiniProfile elements first
            if 'included' in data:
                person_profile_types = [
                    'com.linkedin.voyager.identity.profile.Profile',
                    'com.linkedin.voyager.identity.shared.MiniProfile'
                ]
                
                for target_type in person_profile_types:
                    for element in data['included']:
                        element_type = element.get('$type', '')
                        
                        if element_type == target_type:
                            elem_first = ""
                            elem_last = ""
                            
                            for name_field in ['firstName', 'lastName']:
                                if name_field in element:
                                    name_data = element[name_field]
                                    
                                    name_value = ""
                                    if isinstance(name_data, str):
                                        name_value = name_data.strip()
                                    elif isinstance(name_data, dict) and 'text' in name_data:
                                        name_value = name_data['text'].strip()
                                    
                                    if name_field == 'firstName':
                                        elem_first = name_value
                                    else:
                                        elem_last = name_value
                            
                            if elem_first or elem_last:
                                return f"{elem_first} {elem_last}".strip()
            
            return None
            
        except Exception:
            return None

    def extract_connection_distance(self, data: Dict) -> Optional[int]:
        """Extract connection distance from API response"""
        try:
            # Method 1: Direct distance field
            if 'distance' in data:
                distance_data = data['distance']
                
                if isinstance(distance_data, dict):
                    # Handle LinkedIn's DISTANCE_X format
                    if 'value' in distance_data:
                        distance_value = distance_data['value']
                        if isinstance(distance_value, str) and distance_value.startswith('DISTANCE_'):
                            try:
                                return int(distance_value.split('_')[1])
                            except:
                                pass
                    elif 'distance' in distance_data:
                        return distance_data['distance']
                elif isinstance(distance_data, int):
                    return distance_data
                elif isinstance(distance_data, str) and distance_data.startswith('DISTANCE_'):
                    try:
                        return int(distance_data.split('_')[1])
                    except:
                        pass
            
            # Method 2: Look in included elements
            if 'included' in data:
                for element in data['included']:
                    if 'distance' in element:
                        distance_data = element['distance']
                        
                        if isinstance(distance_data, dict):
                            if 'value' in distance_data and isinstance(distance_data['value'], str) and distance_data['value'].startswith('DISTANCE_'):
                                try:
                                    return int(distance_data['value'].split('_')[1])
                                except:
                                    pass
                            elif 'distance' in distance_data:
                                return distance_data['distance']
                        elif isinstance(distance_data, int):
                            return distance_data
                        elif isinstance(distance_data, str) and distance_data.startswith('DISTANCE_'):
                            try:
                                return int(distance_data.split('_')[1])
                            except:
                                pass
            
            # Method 3: Regex search for patterns
            data_str = json.dumps(data)
            distance_patterns = [
                r'"value":\s*"DISTANCE_(\d+)"',
                r'"distance":\s*(\d+)',
                r'"connectionDegree":\s*(\d+)',
                r'"relationshipDistance":\s*(\d+)'
            ]
            
            for pattern in distance_patterns:
                matches = re.findall(pattern, data_str)
                if matches:
                    return int(matches[0])
            
            return None
            
        except Exception:
            return None

    def check_connection_status(self, profile_url: str) -> Dict:
        """Check connection status with a LinkedIn profile"""
        result = {
            "profile_url": profile_url,
            "is_connected": False,
            "distance": None,
            "connection_status": "Unknown",
            "profile_name": None,
            "error": None
        }
        
        try:
            public_id = self.get_public_identifier_from_url(profile_url)
            if not public_id:
                result["error"] = "Could not extract public identifier from URL"
                return result
                
            # Step 1: Get profile name from profileView endpoint
            try:
                url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/profileView"
                headers = self.session.headers.copy()
                headers.update({
                    "referer": f"https://www.linkedin.com/in/{public_id}/",
                    "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{str(uuid.uuid4())}"
                })
                
                response = self.session.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    name = self.extract_profile_name(data)
                    if name:
                        result["profile_name"] = name
            except Exception:
                pass
                
            # Step 2: Get connection distance from networkinfo endpoint
            try:
                url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/networkinfo"
                headers = self.session.headers.copy()
                headers.update({
                    "referer": f"https://www.linkedin.com/in/{public_id}/",
                    "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{str(uuid.uuid4())}"
                })
                
                response = self.session.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    distance = self.extract_connection_distance(data)
                    
                    if distance is not None:
                        result["distance"] = distance
                        
                        if distance == 1:
                            result["is_connected"] = True
                            result["connection_status"] = "1st degree - Direct connection"
                        elif distance == 2:
                            result["connection_status"] = "2nd degree - Connection of connection"
                        elif distance == 3:
                            result["connection_status"] = "3rd degree - Extended network"
                        else:
                            result["connection_status"] = f"{distance}th degree connection"
                        
                        return result
            except Exception:
                pass
            
            # If we got here, we couldn't determine connection status
            if result.get('profile_name'):
                result["error"] = "Could not determine connection status, but found profile name"
            else:
                result["error"] = "Could not determine connection status"
            return result
            
        except Exception as e:
            result["error"] = f"Exception occurred: {str(e)}"
            return result

    def format_result(self, result: Dict) -> str:
        """Format the result for display"""
        lines = []
        lines.append("=" * 80)
        lines.append("🔗 LINKEDIN CONNECTION STATUS CHECK")
        lines.append("=" * 80)
        
        lines.append(f"🌐 Profile URL: {result['profile_url']}")
        
        if result['profile_name']:
            lines.append(f"👤 Profile Name: {result['profile_name']}")
        
        if result['error']:
            lines.append(f"❌ Error: {result['error']}")
        else:
            if result['is_connected']:
                lines.append("✅ CONNECTION STATUS: CONNECTED")
            else:
                lines.append("❌ CONNECTION STATUS: NOT CONNECTED")
            
            lines.append(f"📊 Connection Details: {result['connection_status']}")
            
            if result['distance'] is not None:
                lines.append(f"📏 Network Distance: {result['distance']} degree(s)")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)

def check_connection(profile_url: str) -> Dict:
    """Simple function to check connection with a LinkedIn profile"""
    checker = LinkedInConnectionChecker()
    result = checker.check_connection_status(profile_url)
    print(checker.format_result(result))
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        profile_url = sys.argv[1]
        check_connection(profile_url)
    else:
        checker = LinkedInConnectionChecker()
        
        print("🔗 LinkedIn Connection Status Checker")
        print("=" * 50)
        
        while True:
            print("\nOptions:")
            print("1. Check connection status with a profile")
            print("2. Exit")
            
            choice = input("\nChoose an option (1-2): ").strip()
            
            if choice == "1":
                profile_url = input("Enter LinkedIn profile URL: ").strip()
                if profile_url:
                    print(f"\n🔍 Checking connection status...")
                    result = checker.check_connection_status(profile_url)
                    print(checker.format_result(result))
                else:
                    print("❌ Please enter a profile URL")
                    
            elif choice == "2":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please choose 1-2.")
                
            input("\nPress Enter to continue...") 