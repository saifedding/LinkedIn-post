#!/usr/bin/env python3
"""
Test script for LinkedIn new contact messaging

This script tests the exact payload format used in the PowerShell script
to ensure our Python implementation works correctly.
"""

import requests
import json
import uuid

def test_message_format():
    """Test the message payload format"""
    
    # Create session with cookies from PowerShell script
    session = requests.Session()
    
    # Add cookies exactly as in PowerShell
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
        "AMCVS_14215E3D5995C57C0A495C55@AdobeOrg": "1",
        "AMCV_14215E3D5995C57C0A495C55@AdobeOrg": "-637568504|MCIDTS|20270|MCMID|27573806750435840703114589459359274076|MCOPTOUT-1751285608s|NONE|vVersion|5.1.1",
        "g_state": '{"i_l":0}',
        "liap": "true",
        "li_at": "AQEDASP6v4EBfhJ7AAABl8BT3OQAAAGX5GBg5E0AocvtLBfU2unQg6KLYHNi6AG83PSJwqQdkZ2kcjhYnS0jlwh0Xy834jLziuj_Kdg3yOwz-L-QrbzlBOjMqHho03KrmOqhKNRdfYXUPajAOyj_oUg_",
        "UserMatchHistory": "AQIopFDFe5LoIwAAAZfBXhApKuszIAJZaXyTcOyZXQdY12yUWz18W0E-pj5F2LJfj9w-GwjhOtHH89ymxGphxiJGi_Kc_ArWucsmtND9hvPSfUwEXF_izt_JYMuTE2QZYx2T2f_bIG_VjX7lJV2EGyixr7vCY7JkHfMylkO5PAyuxL2Chep7GhpJP5ocXNXnls0exgVhn8g2uzxs9eHGc2yLIxaTiqh_q_DfFIyekEjPzGrE7Htey--cyh2Xkzq01RRJWqohQrGMrpHO_PbVN5ItuyU6xEIS3n15tAL5ZoJRnAmJ5T0hYw_redRrD34bYewRR6RrsJTZv_UAqNnnD2VELr97P8tZDMOd5wQM7Fbz8ClCLQ",
        "lidc": "b=VB85:s=V:r=V:a=V:p=V:g=5950:u=788:x=1:i=1751295857:t=1751377341:v=2:sig=AQF0M2-1z0rTjk9jqZtQFPrF42H7id2O"
    }
    
    session.cookies.update(cookies)
    
    # Set User-Agent exactly as PowerShell
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    })
    
    # Headers exactly from PowerShell script
    headers = {
        "authority": "www.linkedin.com",
        "method": "POST", 
        "path": "/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage",
        "scheme": "https",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "csrf-token": "ajax:4763283604314235653",
        "origin": "https://www.linkedin.com",
        "priority": "u=1, i",
        "referer": "https://www.linkedin.com/in/basith-pv/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "x-li-lang": "en_US",
        "x-li-page-instance": "urn:li:page:d_flagship3_profile_view_base;hOn+xkrURFiK118ise1SZw==",
        "x-li-track": '{"clientVersion":"1.13.36800.3","mpVersion":"1.13.36800.3","osName":"web","timezoneOffset":4,"timezone":"Asia/Dubai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2.5,"displayWidth":3840,"displayHeight":2400}',
        "x-restli-protocol-version": "2.0.0",
        "content-type": "text/plain;charset=UTF-8"
    }
    
    # Payload exactly from PowerShell script (but with test message)
    payload = {
        "message": {
            "body": {
                "attributes": [],
                "text": "Test message from Python script"
            },
            "originToken": str(uuid.uuid4()),
            "renderContentUnions": []
        },
        "mailboxUrn": "urn:li:fsd_profile:ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc",
        "trackingId": str(uuid.uuid4())[:16],
        "dedupeByClientGeneratedToken": False,
        "hostRecipientUrns": ["urn:li:fsd_profile:ACoAADEwkRUBRsclphM3WfnP3bk6XgrTK7eNU_g"]
    }
    
    # Convert to JSON and encode as UTF-8 (like PowerShell does)
    json_body = json.dumps(payload, separators=(',', ':'))
    encoded_body = json_body.encode('utf-8')
    
    print("🧪 Testing LinkedIn message format...")
    print(f"📄 Payload: {json_body}")
    print(f"📊 Encoded length: {len(encoded_body)} bytes")
    
    # URL from PowerShell script
    url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage"
    
    try:
        print(f"📤 Sending test message...")
        response = session.post(url, headers=headers, data=encoded_body)
        
        print(f"📈 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Test message sent successfully!")
            try:
                response_data = response.json()
                print(f"📄 Response JSON: {json.dumps(response_data, indent=2)}")
            except:
                print(f"📄 Response Text: {response.text}")
        else:
            print(f"❌ Test failed. Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_message_format() 