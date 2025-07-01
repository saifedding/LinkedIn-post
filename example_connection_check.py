#!/usr/bin/env python3
"""
Example script showing how to use the LinkedIn Connection Checker
"""

from linkedin_connection_checker import check_connection, LinkedInConnectionChecker

def main():
    """Example usage of the LinkedIn Connection Checker"""
    
    # Example LinkedIn profile URLs to check
    # Replace these with actual LinkedIn profile URLs
    test_profiles = [
        "https://www.linkedin.com/in/example-profile-1/",
        "https://www.linkedin.com/in/example-profile-2/",
        "https://www.linkedin.com/in/example-profile-3/"
    ]
    
    print("🔗 LinkedIn Connection Status Checker - Example Usage")
    print("=" * 60)
    
    # Method 1: Using the simple function
    print("\n📝 Method 1: Using the simple check_connection() function")
    print("-" * 50)
    
    for profile_url in test_profiles:
        print(f"\n🔍 Checking: {profile_url}")
        result = check_connection(profile_url)
        
        # You can access the result data
        if result['is_connected']:
            print(f"✅ Connected with {result['profile_name']} (Distance: {result['distance']})")
        elif result['error']:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"❌ Not connected with {result['profile_name'] or 'Unknown'}")
    
    print("\n" + "=" * 60)
    
    # Method 2: Using the class directly for more control
    print("\n📝 Method 2: Using LinkedInConnectionChecker class directly")
    print("-" * 50)
    
    checker = LinkedInConnectionChecker()
    
    batch_results = []
    for profile_url in test_profiles:
        print(f"\n🔍 Checking: {profile_url}")
        result = checker.check_connection_status(profile_url)
        batch_results.append(result)
        
        # Custom processing of results
        if result['error']:
            print(f"❌ Failed to check: {result['error']}")
        else:
            status = "✅ CONNECTED" if result['is_connected'] else "❌ NOT CONNECTED"
            name = result['profile_name'] or "Unknown"
            distance = result['distance'] or "Unknown"
            print(f"{status} - {name} (Distance: {distance})")
    
    # Summary of all checks
    print("\n" + "=" * 60)
    print("📊 SUMMARY OF ALL CONNECTION CHECKS")
    print("=" * 60)
    
    connected_count = sum(1 for r in batch_results if r['is_connected'])
    total_count = len(batch_results)
    error_count = sum(1 for r in batch_results if r['error'])
    
    print(f"Total profiles checked: {total_count}")
    print(f"Connected profiles: {connected_count}")
    print(f"Not connected: {total_count - connected_count - error_count}")
    print(f"Errors: {error_count}")
    
    # Show connected profiles
    if connected_count > 0:
        print(f"\n✅ Connected profiles:")
        for result in batch_results:
            if result['is_connected']:
                name = result['profile_name'] or "Unknown"
                distance = result['distance']
                print(f"  - {name} (Distance: {distance})")

if __name__ == "__main__":
    # Interactive mode for testing with real URLs
    print("🔗 LinkedIn Connection Checker - Interactive Example")
    print("=" * 50)
    
    choice = input("Would you like to:\n1. Run example with dummy URLs\n2. Test with your own URL\nChoose (1 or 2): ").strip()
    
    if choice == "1":
        print("\n⚠️ Running with example URLs (these will likely fail)")
        main()
    elif choice == "2":
        profile_url = input("\nEnter a LinkedIn profile URL to test: ").strip()
        if profile_url:
            print(f"\n🔍 Testing connection with: {profile_url}")
            result = check_connection(profile_url)
        else:
            print("❌ No URL provided")
    else:
        print("❌ Invalid choice") 