#!/usr/bin/env python3
"""
Debug test script to analyze LinkedIn API responses
This will help us understand the actual structure of the data
"""

import requests
import json
import sys
from linkedin_connection_checker import LinkedInConnectionChecker

def debug_profile_response(profile_url: str):
    """Debug the API response for a profile"""
    
    checker = LinkedInConnectionChecker()
    
    # Extract public ID
    public_id = checker.get_public_identifier_from_url(profile_url)
    if not public_id:
        print("❌ Could not extract public ID")
        return
    
    print(f"🔍 Debugging profile: {public_id}")
    print("=" * 60)
    
    # Try the profileView endpoint
    url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/profileView"
    
    headers = checker.session.headers.copy()
    headers.update({
        "referer": f"https://www.linkedin.com/in/{public_id}/",
        "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;12345678"
    })
    
    print(f"📞 Making request to: {url}")
    
    try:
        response = checker.session.get(url, headers=headers)
        print(f"📈 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"📊 Response Keys: {list(data.keys())}")
            
            # Check main level fields
            print("\n🔍 MAIN LEVEL ANALYSIS:")
            print("-" * 40)
            
            for key, value in data.items():
                if key == "included":
                    print(f"  {key}: {len(value)} elements")
                elif isinstance(value, dict):
                    print(f"  {key}: dict with {len(value)} keys -> {list(value.keys())[:3]}...")
                elif isinstance(value, list):
                    print(f"  {key}: list with {len(value)} items")
                else:
                    print(f"  {key}: {type(value)} -> {str(value)[:50]}...")
            
            # Analyze included elements
            if 'included' in data:
                print(f"\n🔍 INCLUDED ELEMENTS ANALYSIS:")
                print("-" * 40)
                
                element_types = {}
                for i, element in enumerate(data['included']):
                    element_type = element.get('$type', 'unknown')
                    entity_urn = element.get('entityUrn', '')
                    
                    if element_type not in element_types:
                        element_types[element_type] = []
                    element_types[element_type].append(i)
                    
                    print(f"  Element {i}: {element_type}")
                    if entity_urn:
                        print(f"    URN: {entity_urn}")
                    
                    # Check for name fields
                    name_fields = []
                    for field in ['firstName', 'lastName', 'name', 'title']:
                        if field in element:
                            name_fields.append(f"{field}={element[field]}")
                    
                    if name_fields:
                        print(f"    Names: {', '.join(name_fields)}")
                    
                    # Check for distance/connection fields
                    connection_fields = []
                    for field in ['distance', 'connectionDegree', 'relationshipDistance']:
                        if field in element:
                            connection_fields.append(f"{field}={element[field]}")
                    
                    if connection_fields:
                        print(f"    Connection: {', '.join(connection_fields)}")
                
                print(f"\n📊 Element Types Summary:")
                for element_type, indices in element_types.items():
                    print(f"  {element_type}: {len(indices)} elements (indices: {indices[:5]}...)")
            
            # Save full response
            filename = f"debug_{public_id}_full.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"\n💾 Full response saved to: {filename}")
            
            # Look for specific patterns
            print(f"\n🔍 SEARCHING FOR PATTERNS:")
            print("-" * 40)
            
            data_str = json.dumps(data)
            
            # Search for distance patterns
            import re
            patterns = [
                (r'"distance":\s*(\d+)', "distance field"),
                (r'"connectionDegree":\s*(\d+)', "connectionDegree field"),  
                (r'"connected"', "connected keyword"),
                (r'"1st"', "1st degree keyword"),
                (r'"2nd"', "2nd degree keyword"),
                (r'firstName.*?text.*?([A-Za-z]+)', "firstName patterns"),
                (r'lastName.*?text.*?([A-Za-z]+)', "lastName patterns")
            ]
            
            for pattern, description in patterns:
                matches = re.findall(pattern, data_str, re.IGNORECASE)
                if matches:
                    print(f"  {description}: {matches[:5]}")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        profile_url = sys.argv[1]
        debug_profile_response(profile_url)
    else:
        print("Usage: python test_debug_connection.py <linkedin_profile_url>")
        print("Example: python test_debug_connection.py https://www.linkedin.com/in/johndoe/") 