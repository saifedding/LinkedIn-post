#!/usr/bin/env python3
"""
Simple LinkedIn URN Getter
Get mailbox_urn and conversation_urn by person name
"""

from linkedin_conversation_extractor import LinkedInConversationExtractor

def get_linkedin_urns_by_name(name: str):
    """
    Get LinkedIn URNs for a person by their name
    
    Args:
        name: Person's name (first name, last name, or LinkedIn public identifier)
        
    Usage:
        get_linkedin_urns_by_name("oussama")
        get_linkedin_urns_by_name("oussamagaham") 
        get_linkedin_urns_by_name("John Doe")
    """
    
    print(f"🔍 Looking up LinkedIn URNs for: '{name}'")
    print("-" * 50)
    
    try:
        # Create extractor and get URNs
        extractor = LinkedInConversationExtractor()
        result = extractor.get_urns_by_name(name)
        
        if result:
            print("✅ FOUND!")
            print(f"📋 Full Name: {result['full_name']}")
            print(f"🔗 Public ID: {result['public_identifier']}")
            print()
            print("📋 URNs for your messaging script:")
            print(f'mailbox_urn = "{result["mailbox_urn"]}"')
            print(f'conversation_urn = "{result["conversation_urn"]}"')
            print()
            print("📊 Additional Info:")
            print(f"   Last Activity: {result['last_activity']}")
            print(f"   Unread Messages: {result['unread_count']}")
            
            return result
        else:
            print("❌ NOT FOUND")
            print("💡 Try:")
            print("   - First name only (e.g., 'john')")
            print("   - Full name (e.g., 'john doe')")
            print("   - LinkedIn public identifier")
            print("   - Make sure you have an existing conversation with this person")
            
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_all_conversation_mapping():
    """Get a complete mapping of all your LinkedIn conversations"""
    
    print("🔍 Getting all LinkedIn conversation mappings...")
    print("=" * 70)
    
    try:
        extractor = LinkedInConversationExtractor()
        
        # Get all conversations
        api_response = extractor.get_conversations()
        if not api_response:
            print("❌ Failed to get conversations")
            return {}
        
        conversations = extractor.extract_conversation_data(api_response)
        name_mapping = extractor.create_name_mapping(conversations)
        
        print(f"📊 Found {len(conversations)} conversations")
        print(f"🔑 Created {len(name_mapping)} name mappings")
        print()
        
        # Print organized mapping
        print("📋 NAME → URN MAPPING:")
        print("-" * 70)
        
        for name, data in sorted(name_mapping.items()):
            print(f"'{name}' →")
            print(f"  Full Name: {data['full_name']}")
            print(f"  mailbox_urn = \"{data['mailbox_urn']}\"")
            print(f"  conversation_urn = \"{data['conversation_urn']}\"")
            print()
        
        return name_mapping
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line usage: python get_urns.py "oussama"
        name = " ".join(sys.argv[1:])
        get_linkedin_urns_by_name(name)
    else:
        # Interactive usage
        print("🚀 LinkedIn URN Getter")
        print("=" * 50)
        
        while True:
            print("\nOptions:")
            print("1. Get URNs for specific person")
            print("2. Show all conversation mappings") 
            print("3. Exit")
            
            choice = input("\nChoose an option (1-3): ").strip()
            
            if choice == "1":
                name = input("Enter person's name: ").strip()
                if name:
                    print()
                    get_linkedin_urns_by_name(name)
                else:
                    print("❌ Please enter a name")
                    
            elif choice == "2":
                print()
                get_all_conversation_mapping()
                
            elif choice == "3":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please choose 1-3.")
                
            input("\nPress Enter to continue...")

# Quick examples for testing
def examples():
    """Show some examples"""
    print("📋 EXAMPLES:")
    print("=" * 50)
    
    # Example 1: Get URNs for Oussama
    print("Example 1: Get URNs for Oussama")
    result1 = get_linkedin_urns_by_name("oussama")
    
    print("\n" + "-" * 50)
    
    # Example 2: Get URNs by public identifier  
    print("Example 2: Get URNs by public identifier")
    result2 = get_linkedin_urns_by_name("oussamagaham")
    
    return result1, result2 