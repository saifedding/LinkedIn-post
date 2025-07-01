#!/usr/bin/env python3
"""
LinkedIn Connection Checker

This script checks if a given LinkedIn profile is connected with you.
Uses the LinkedIn voyager API to check the connection distance.

Distance = 1: Direct connection (1st degree)
Distance = 2: 2nd degree connection (connection of connection)
Distance = 3: 3rd degree or more
Distance = None/0: Not connected or profile not accessible
"""

import requests
import json
import re
import sys
from typing import Dict, Optional, Tuple
from urllib.parse import quote
import uuid

class LinkedInConnectionChecker:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session with cookies and headers from existing scripts"""
        
        # Updated cookies from your existing scripts
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
        
        # Set headers similar to existing scripts
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
                # Extract everything after '/in/' and remove trailing slash
                public_id = profile_url.split('/in/')[-1].strip('/')
                # Remove any query parameters or fragments
                public_id = public_id.split('?')[0].split('#')[0]
                return public_id
        except Exception as e:
            print(f"❌ Error extracting public ID from URL: {e}")
        return None

    def check_connection_status(self, profile_url: str) -> Dict:
        """
        Check connection status with a LinkedIn profile
        
        Args:
            profile_url: LinkedIn profile URL
            
        Returns:
            Dict containing connection status and details
        """
        result = {
            "profile_url": profile_url,
            "is_connected": False,
            "distance": None,
            "connection_status": "Unknown",
            "profile_name": None,
            "error": None
        }
        
        try:
            # Extract public identifier
            public_id = self.get_public_identifier_from_url(profile_url)
            if not public_id:
                result["error"] = "Could not extract public identifier from URL"
                return result
                
            print(f"🔍 Checking connection with profile: {public_id}")
            
            # Method 1: Try the profileView endpoint (for name, basic info)
            connection_data = self.check_via_profile_view(public_id)
            if connection_data:
                # Keep the profile name from this response
                if connection_data.get('profile_name'):
                    result['profile_name'] = connection_data['profile_name']
                
                # If we found distance info, use it
                if connection_data.get('distance') is not None:
                    result.update(connection_data)
                    return result
            
            # Method 2: Try relationship endpoints (specifically for connection info)
            relationship_data = self.check_via_relationship_endpoint(public_id)
            if relationship_data and relationship_data.get('distance') is not None:
                # Merge with existing data (keep the name from profileView if we have it)
                if result.get('profile_name'):
                    relationship_data['profile_name'] = result['profile_name']
                result.update(relationship_data)
                return result
                
            # Method 3: Try profile actions endpoint (for connection buttons/status)
            actions_data = self.check_via_profile_actions(public_id)
            if actions_data and actions_data.get('distance') is not None:
                # Merge with existing data
                if result.get('profile_name'):
                    actions_data['profile_name'] = result['profile_name']
                result.update(actions_data)
                return result
            
            # Method 4: Try the general identity endpoint
            identity_data = self.check_via_identity_api(public_id)
            if identity_data:
                # Merge with existing data
                if result.get('profile_name'):
                    identity_data['profile_name'] = result['profile_name']
                result.update(identity_data)
                return result
                
            # Method 5: Try hovering card endpoint (last resort)
            card_data = self.check_via_hovering_card(public_id)
            if card_data:
                # Merge with existing data
                if result.get('profile_name'):
                    card_data['profile_name'] = result['profile_name']
                result.update(card_data)
                return result
                
            # If we got here, we couldn't determine connection status but we might have the name
            if result.get('profile_name'):
                result["error"] = "Could not determine connection status, but found profile name"
            else:
                result["error"] = "Could not determine connection status using any method"
            return result
            
        except Exception as e:
            result["error"] = f"Exception occurred: {str(e)}"
            return result

    def check_via_profile_view(self, public_id: str) -> Optional[Dict]:
        """Check connection via profileView endpoint"""
        try:
            url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/profileView"
            
            headers = self.session.headers.copy()
            headers.update({
                "referer": f"https://www.linkedin.com/in/{public_id}/",
                "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{str(uuid.uuid4())}"
            })
            
            print(f"📞 Trying profileView endpoint...")
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save raw response for debugging
                import os
                debug_dir = "debug_responses"
                if not os.path.exists(debug_dir):
                    os.makedirs(debug_dir)
                
                debug_file = os.path.join(debug_dir, f"profileView_{public_id}.json")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"💾 Saved raw response to: {debug_file}")
                
                return self.extract_connection_info(data, "profileView")
            else:
                print(f"❌ ProfileView endpoint failed: {response.status_code}")
                print(f"Response text: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ ProfileView method error: {e}")
            
        return None

    def check_via_identity_api(self, public_id: str) -> Optional[Dict]:
        """Check connection via identity profiles endpoint"""
        try:
            url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}"
            
            headers = self.session.headers.copy()
            headers.update({
                "referer": f"https://www.linkedin.com/in/{public_id}/",
                "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{str(uuid.uuid4())}"
            })
            
            print(f"📞 Trying identity API endpoint...")
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save raw response for debugging
                import os
                debug_dir = "debug_responses"
                if not os.path.exists(debug_dir):
                    os.makedirs(debug_dir)
                
                debug_file = os.path.join(debug_dir, f"identity_{public_id}.json")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"💾 Saved raw response to: {debug_file}")
                
                return self.extract_connection_info(data, "identity")
            else:
                print(f"❌ Identity API endpoint failed: {response.status_code}")
                print(f"Response text: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Identity API method error: {e}")
            
        return None

    def check_via_hovering_card(self, public_id: str) -> Optional[Dict]:
        """Check connection via hovering card endpoint"""
        try:
            # First get the profile to find the URN
            profile_urn = self.get_profile_urn_for_public_id(public_id)
            if not profile_urn:
                return None
                
            # Extract just the ID part
            urn_id = profile_urn.split(':')[-1] if ':' in profile_urn else profile_urn
            
            url = f"https://www.linkedin.com/voyager/api/identity/profiles/{urn_id}/profileContactInfo"
            
            headers = self.session.headers.copy()
            headers.update({
                "referer": f"https://www.linkedin.com/in/{public_id}/",
                "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{str(uuid.uuid4())}"
            })
            
            print(f"📞 Trying hovering card endpoint...")
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return self.extract_connection_info(data, "hoveringCard")
            else:
                print(f"❌ Hovering card endpoint failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Hovering card method error: {e}")
            
        return None

    def check_via_relationship_endpoint(self, public_id: str) -> Optional[Dict]:
        """Check connection via relationship/network endpoint"""
        try:
            # Try multiple relationship endpoints
            relationship_endpoints = [
                f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/networkinfo",
                f"https://www.linkedin.com/voyager/api/relationships/connectionDistance?profiles=List({public_id})",
                f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/relationship",
                f"https://www.linkedin.com/voyager/api/relationships/relationship/{public_id}",
                f"https://www.linkedin.com/voyager/api/identity/shared/connections/{public_id}"
            ]
            
            headers = self.session.headers.copy()
            headers.update({
                "referer": f"https://www.linkedin.com/in/{public_id}/",
                "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{str(uuid.uuid4())}"
            })
            
            for endpoint in relationship_endpoints:
                try:
                    print(f"📞 Trying relationship endpoint: {endpoint}")
                    response = self.session.get(endpoint, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Save debug data
                        import os
                        debug_dir = "debug_responses"
                        if not os.path.exists(debug_dir):
                            os.makedirs(debug_dir)
                        
                        endpoint_name = endpoint.split('/')[-1]
                        debug_file = os.path.join(debug_dir, f"relationship_{endpoint_name}_{public_id}.json")
                        with open(debug_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2)
                        print(f"💾 Saved relationship response to: {debug_file}")
                        
                        result = self.extract_connection_info(data, f"relationship_{endpoint_name}")
                        if result and result.get('distance') is not None:
                            return result
                            
                    else:
                        print(f"❌ Endpoint failed: {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Error with endpoint {endpoint}: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Relationship endpoint method error: {e}")
            
        return None

    def check_via_profile_actions(self, public_id: str) -> Optional[Dict]:
        """Check connection via profile actions/cta endpoint"""
        try:
            # Try the profile CTA (Call To Action) endpoint which often has connection info
            url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/profileActions"
            
            headers = self.session.headers.copy()
            headers.update({
                "referer": f"https://www.linkedin.com/in/{public_id}/",
                "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{str(uuid.uuid4())}"
            })
            
            print(f"📞 Trying profile actions endpoint...")
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save debug data
                import os
                debug_dir = "debug_responses"
                if not os.path.exists(debug_dir):
                    os.makedirs(debug_dir)
                
                debug_file = os.path.join(debug_dir, f"profileActions_{public_id}.json")
                with open(debug_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"💾 Saved profile actions response to: {debug_file}")
                
                return self.extract_connection_info(data, "profileActions")
            else:
                print(f"❌ Profile actions endpoint failed: {response.status_code}")
                print(f"Response text: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Profile actions method error: {e}")
            
        return None

    def get_profile_urn_for_public_id(self, public_id: str) -> Optional[str]:
        """Get profile URN for a public identifier"""
        try:
            url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'entityUrn' in data:
                    return data['entityUrn']
                    
                # Check in included elements
                if 'included' in data:
                    for element in data['included']:
                        if 'entityUrn' in element and 'fsd_profile' in element['entityUrn']:
                            return element['entityUrn']
                            
        except Exception as e:
            print(f"❌ Error getting profile URN: {e}")
            
        return None

    def extract_connection_info(self, data: Dict, source: str) -> Optional[Dict]:
        """Extract connection information from API response"""
        try:
            result = {
                "is_connected": False,
                "distance": None,
                "connection_status": "Not Connected",
                "profile_name": None,
                "source": source
            }
            
            # DEBUG: Print response structure to understand the data
            print(f"🔍 DEBUG: Analyzing {source} response...")
            if 'included' in data:
                print(f"📊 Found {len(data['included'])} included elements")
            
            # Extract profile name with improved logic
            name = self.extract_profile_name(data)
            if name:
                result["profile_name"] = name
                print(f"👤 Extracted name: {name}")
            
            # Look for distance information in various places
            distance = None
            
            # Method 1: Direct distance field
            if 'distance' in data:
                distance_data = data['distance']
                print(f"🔍 Found direct distance field: {distance_data}")
                
                if isinstance(distance_data, dict):
                    # Handle LinkedIn's DISTANCE_X format
                    if 'value' in distance_data:
                        distance_value = distance_data['value']
                        if isinstance(distance_value, str) and distance_value.startswith('DISTANCE_'):
                            try:
                                distance = int(distance_value.split('_')[1])
                                print(f"🔍 Parsed distance from {distance_value}: {distance}")
                            except:
                                pass
                    elif 'distance' in distance_data:
                        distance = distance_data['distance']
                elif isinstance(distance_data, int):
                    distance = distance_data
                elif isinstance(distance_data, str) and distance_data.startswith('DISTANCE_'):
                    try:
                        distance = int(distance_data.split('_')[1])
                        print(f"🔍 Parsed distance from {distance_data}: {distance}")
                    except:
                        pass
            
            # Method 2: Look in included elements for distance
            if distance is None and 'included' in data:
                for i, element in enumerate(data['included']):
                    if 'distance' in element:
                        print(f"🔍 Found distance in element {i}: {element['distance']}")
                        distance_data = element['distance']
                        
                        if isinstance(distance_data, dict):
                            # Handle LinkedIn's DISTANCE_X format
                            if 'value' in distance_data and isinstance(distance_data['value'], str) and distance_data['value'].startswith('DISTANCE_'):
                                try:
                                    distance = int(distance_data['value'].split('_')[1])
                                    print(f"🔍 Parsed distance from element {i}: {distance}")
                                    break
                                except:
                                    pass
                            elif 'distance' in distance_data:
                                distance = distance_data['distance']
                                break
                        elif isinstance(distance_data, int):
                            distance = distance_data
                            break
                        elif isinstance(distance_data, str) and distance_data.startswith('DISTANCE_'):
                            try:
                                distance = int(distance_data.split('_')[1])
                                print(f"🔍 Parsed distance from element {i}: {distance}")
                                break
                            except:
                                pass
                    
                    # Also check for relationship indicators
                    if 'connectionDegree' in element:
                        print(f"🔍 Found connectionDegree in element {i}: {element['connectionDegree']}")
                        distance = element['connectionDegree']
                        break
                    
                    # Check for relatedtoviewer field
                    if 'relationshipDistance' in element:
                        print(f"🔍 Found relationshipDistance in element {i}: {element['relationshipDistance']}")
                        distance = element['relationshipDistance']
                        break
            
            # Method 3: Search for specific connection patterns in response
            if distance is None:
                data_str = json.dumps(data)
                print(f"🔍 Searching for connection patterns in response...")
                
                # Look for specific distance patterns
                import re
                distance_patterns = [
                    (r'"value":\s*"DISTANCE_(\d+)"', "DISTANCE_X format"),
                    (r'"distance":\s*(\d+)', "distance field"),
                    (r'"connectionDegree":\s*(\d+)', "connectionDegree field"),
                    (r'"relationshipDistance":\s*(\d+)', "relationshipDistance field"),
                    (r'"degree":\s*(\d+)', "degree field")
                ]
                
                for pattern, description in distance_patterns:
                    matches = re.findall(pattern, data_str)
                    if matches:
                        distance = int(matches[0])
                        print(f"🔍 Found distance via pattern '{description}': {distance}")
                        break
                
                # Look for text indicators
                if distance is None:
                    data_str_lower = data_str.lower()
                    if '"connected"' in data_str_lower or '"1st"' in data_str_lower:
                        distance = 1
                        print("🔍 Found connection indicator: 1st degree")
                    elif '"2nd"' in data_str_lower:
                        distance = 2
                        print("🔍 Found connection indicator: 2nd degree")
                    elif '"3rd"' in data_str_lower:
                        distance = 3
                        print("🔍 Found connection indicator: 3rd degree")
            
            # Method 4: Check for messaging availability
            if distance is None:
                if self.check_messaging_availability(data):
                    distance = 1
                    print("🔍 Inferred connection from messaging availability")
            
            # Print final distance result
            if distance is not None:
                print(f"📏 Final distance: {distance}")
            else:
                print("❌ Could not determine connection distance")
            
            # Set the results based on distance
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
            
        except Exception as e:
            print(f"❌ Error extracting connection info: {e}")
            import traceback
            traceback.print_exc()
            return None

    def extract_profile_name(self, data: Dict) -> Optional[str]:
        """Extract profile name from API response"""
        try:
            print(f"🔍 DEBUG: Looking for profile name...")
            
            # Method 1: Direct fields in main data
            for name_field in ['firstName', 'lastName', 'name', 'fullName']:
                if name_field in data:
                    name_data = data[name_field]
                    print(f"🔍 Found {name_field}: {name_data}")
                    if isinstance(name_data, str) and name_data.strip():
                        return name_data.strip()
                    elif isinstance(name_data, dict) and 'text' in name_data:
                        return name_data['text'].strip()
            
            # Method 2: Combine firstName and lastName from main data
            first_name = ""
            last_name = ""
            
            if 'firstName' in data:
                first_data = data['firstName']
                if isinstance(first_data, str):
                    first_name = first_data.strip()
                elif isinstance(first_data, dict) and 'text' in first_data:
                    first_name = first_data['text'].strip()
                print(f"🔍 First name from main: '{first_name}'")
            
            if 'lastName' in data:
                last_data = data['lastName']
                if isinstance(last_data, str):
                    last_name = last_data.strip()
                elif isinstance(last_data, dict) and 'text' in last_data:
                    last_name = last_data['text'].strip()
                print(f"🔍 Last name from main: '{last_name}'")
            
            if first_name or last_name:
                full_name = f"{first_name} {last_name}".strip()
                print(f"🔍 Combined name from main: '{full_name}'")
                return full_name
            
            # Method 3: Look in included elements for person profile
            if 'included' in data:
                print(f"🔍 Searching through {len(data['included'])} included elements...")
                
                # First, look for the main Profile and MiniProfile elements (most reliable)
                person_profile_types = [
                    'com.linkedin.voyager.identity.profile.Profile',
                    'com.linkedin.voyager.identity.shared.MiniProfile'
                ]
                
                for target_type in person_profile_types:
                    for i, element in enumerate(data['included']):
                        element_type = element.get('$type', '')
                        
                        if element_type == target_type:
                            print(f"🔍 Found {target_type} at element {i}")
                            
                            # Try to extract names from this element
                            elem_first = ""
                            elem_last = ""
                            
                            for name_field in ['firstName', 'lastName']:
                                if name_field in element:
                                    name_data = element[name_field]
                                    print(f"🔍 Element {i} {name_field}: {name_data}")
                                    
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
                                full_name = f"{elem_first} {elem_last}".strip()
                                print(f"🔍 Found person name in {target_type}: '{full_name}'")
                                return full_name
                
                # Fallback: look for any profile-related elements
                for i, element in enumerate(data['included']):
                    element_type = element.get('$type', '')
                    entity_urn = element.get('entityUrn', '')
                    
                    # Look for person-specific indicators, but exclude companies
                    is_person = (
                        'profile' in element_type.lower() and 
                        'company' not in element_type.lower() and
                        'minicompany' not in element_type.lower()
                    )
                    
                    if is_person:
                        print(f"🔍 Found person-related element {i}: {element_type}")
                        
                        # Try to extract names from this element
                        elem_first = ""
                        elem_last = ""
                        
                        for name_field in ['firstName', 'lastName']:
                            if name_field in element:
                                name_data = element[name_field]
                                print(f"🔍 Element {i} {name_field}: {name_data}")
                                
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
                            full_name = f"{elem_first} {elem_last}".strip()
                            print(f"🔍 Found person name in element {i}: '{full_name}'")
                            return full_name
                
                # Fallback: look for any firstName/lastName combination
                print(f"🔍 Fallback: looking for any firstName/lastName in elements...")
                for i, element in enumerate(data['included']):
                    if 'firstName' in element and 'lastName' in element:
                        first_data = element['firstName']
                        last_data = element['lastName']
                        
                        elem_first = ""
                        elem_last = ""
                        
                        if isinstance(first_data, str):
                            elem_first = first_data.strip()
                        elif isinstance(first_data, dict) and 'text' in first_data:
                            elem_first = first_data['text'].strip()
                        
                        if isinstance(last_data, str):
                            elem_last = last_data.strip()
                        elif isinstance(last_data, dict) and 'text' in last_data:
                            elem_last = last_data['text'].strip()
                        
                        if elem_first or elem_last:
                            full_name = f"{elem_first} {elem_last}".strip()
                            print(f"🔍 Found fallback name in element {i}: '{full_name}'")
                            return full_name
            
            print(f"❌ Could not extract profile name")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting name: {e}")
            import traceback
            traceback.print_exc()
            return None

    def check_messaging_availability(self, data: Dict) -> bool:
        """Check if messaging is available (indication of connection)"""
        try:
            data_str = json.dumps(data).lower()
            messaging_indicators = [
                '"canmessage"',
                '"messageable"',
                '"messaging"',
                '"sendmessage"'
            ]
            
            for indicator in messaging_indicators:
                if indicator in data_str:
                    return True
                    
        except Exception:
            pass
            
        return False

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
            
            if 'source' in result:
                lines.append(f"🔍 Data Source: {result['source']}")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)

def check_connection(profile_url: str) -> Dict:
    """
    Simple function to check connection with a LinkedIn profile
    
    Args:
        profile_url: LinkedIn profile URL
        
    Returns:
        Dict with connection status information
    """
    checker = LinkedInConnectionChecker()
    result = checker.check_connection_status(profile_url)
    print(checker.format_result(result))
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line usage: python linkedin_connection_checker.py "https://linkedin.com/in/johndoe"
        profile_url = sys.argv[1]
        check_connection(profile_url)
    else:
        # Interactive usage
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
                    print("\n🔍 Checking connection status...")
                    result = checker.check_connection_status(profile_url)
                    print(checker.format_result(result))
                    
                    # Ask if they want to save to file
                    save = input("\n💾 Save result to file? (y/n): ").strip().lower()
                    if save == 'y':
                        filename = f"connection_check_{result.get('profile_name', 'profile').replace(' ', '_').lower()}.json"
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2)
                        print(f"✅ Result saved to: {filename}")
                else:
                    print("❌ Please enter a profile URL")
                    
            elif choice == "2":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please choose 1-2.")
                
            input("\nPress Enter to continue...") 