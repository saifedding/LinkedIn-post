# LinkedIn Message Sender

Tools for programmatically sending messages on LinkedIn.

## Features

- PowerShell script for sending LinkedIn messages
- Python scripts for extracting conversation URNs by name
- Profile URN extractor for messaging new contacts
- Utilities for managing LinkedIn messaging

## Python Tools

### Get URNs by Name

Extract URNs for existing conversations using the person's name:

```
python get_urns.py
```

This interactive script will:
- Fetch all your LinkedIn conversations
- Map contacts' names to their URNs
- Let you search for people by name to get their URNs

### Extract Profile URNs

Extract URNs directly from a LinkedIn profile URL (for messaging new contacts):

```
python get_profile_urns.py https://www.linkedin.com/in/johndoe/
```

This script helps you:
- Get the recipient's URN (`hostRecipientUrns`) from their profile URL
- Format a ready-to-use API request payload
- Generate PowerShell-compatible code for sending messages

For more details, see [README_PROFILE_URN.md](README_PROFILE_URN.md)

### Send Messages in Python

Send messages directly using Python:

```
python send_message.py
```

Enter a name or LinkedIn URL when prompted, and the script will:
- Look up the necessary URNs
- Send your message directly via the LinkedIn API
- Provide feedback on the message delivery status

### Message New Contacts

Send messages to LinkedIn profiles you've never contacted before:

```
python message_new_contact.py https://www.linkedin.com/in/johndoe/ "Hello John, nice to connect!"
```

This script:
- Extracts the profile URN from the LinkedIn URL
- Uses the exact same format as the PowerShell script for new contacts
- Sends messages via the `hostRecipientUrns` parameter
- Matches the headers and payload structure for maximum compatibility

You can also run it interactively:
```
python message_new_contact.py https://www.linkedin.com/in/johndoe/
# You'll be prompted to enter your message
```

## PowerShell Usage

The script provides a simple way to send LinkedIn messages using PowerShell.

### Prerequisites

- PowerShell 5.1 or higher
- Valid LinkedIn authentication cookies

### Sending a Message

```powershell
# Basic usage
.\send_linkedin_message.ps1 -MessageText "Hello, this is a test message" -ConversationUrn "urn:li:msg_conversation:(urn:li:fsd_profile:ACoAACP6v4EBbrCCbpgNB017RQfDpIJA4cgt_oc,2-OTkxOWNhY2YtYWY1ZC00OTNjLWE5YzItMmZiYjFhYzE2MjE1XzEwMA==)"

# Using a config file
.\send_linkedin_message.ps1 -MessageText "Hello, this is a test message" -ConversationUrn "urn:li:msg_conversation:(urn:li:fsd_profile:YOUR_PROFILE_ID,CONVERSATION_ID)" -ConfigFile "my_linkedin_config.json"

# Specifying a profile ID
.\send_linkedin_message.ps1 -MessageText "Hello, this is a test message" -ConversationUrn "urn:li:msg_conversation:(urn:li:fsd_profile:YOUR_PROFILE_ID,CONVERSATION_ID)" -ProfileId "YOUR_PROFILE_ID"
```

### Parameters

- **MessageText**: The content of your message
- **ConversationUrn**: The URN of the conversation you want to send the message to
- **ConfigFile** (optional): Path to a JSON config file containing LinkedIn cookies
- **ProfileId** (optional): Your LinkedIn profile ID

### Finding the Conversation URN

1. Open the LinkedIn conversation in your browser
2. The URL will look something like: `https://www.linkedin.com/messaging/thread/2-OTkxOWNhY2YtYWY1ZC00OTNjLWE5YzItMmZiYjFhYzE2MjE1XzEwMA==/`
3. Use the following format for the URN:
   ```
   urn:li:msg_conversation:(urn:li:fsd_profile:YOUR_PROFILE_ID,CONVERSATION_ID_FROM_URL)
   ```

## Configuration

There are two ways to set up the configuration:

### Option 1: Using the Extract Cookies Helper

The easiest way to get started is to use the included helper script:

```powershell
.\extract_cookies.ps1
```

This interactive script will:
1. Prompt you for your LinkedIn profile ID
2. Guide you through collecting essential cookies from your browser
3. Generate a config file automatically

You can also specify a custom output file:
```powershell
.\extract_cookies.ps1 -OutputFile "my_custom_config.json"
```

### Option 2: Manual Configuration

Alternatively, you can set up the configuration manually:

1. Copy the template file:
   ```
   cp linkedin_config_template.json linkedin_config.json
   ```

2. Edit the file to include your cookies:
   ```json
   {
     "profile_id": "YOUR_LINKEDIN_PROFILE_ID",
     "cookies": [
       {
         "name": "li_at",
         "value": "YOUR_LI_AT_VALUE",
         "path": "/",
         "domain": ".www.linkedin.com"
       },
       // Add more cookies here...
     ],
     "csrf_token": "ajax:YOUR_CSRF_TOKEN"
   }
   ```

3. Getting your cookies:
   - Open LinkedIn in your browser
   - Open Developer Tools (F12)
   - Go to the "Application" tab
   - Under "Storage" click on "Cookies"
   - Find the cookies for the linkedin.com domain
   - Copy the values to your config file

## File Structure

- `send_linkedin_message.ps1` - PowerShell script for sending messages
- `extract_cookies.ps1` - Helper script to generate configuration
- `linkedin_config_template.json` - Template for configuration
- `send_message.py` - Python script for sending messages to existing contacts
- `message_new_contact.py` - Python script for messaging new contacts (never contacted before)
- `get_urns.py` - Python script to extract URNs by contact name
- `get_profile_urns.py` - Python script to extract URNs from profile URLs
- `linkedin_conversation_extractor.py` - Core library for conversation data extraction
- `test_new_message.py` - Test script to verify new contact messaging functionality

## Disclaimer

This script is provided for educational purposes only. Use it responsibly and in accordance with LinkedIn's terms of service. 