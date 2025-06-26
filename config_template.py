# LinkedIn Authentication Configuration Template
# INSTRUCTIONS: 
# 1. Copy this file to 'config.py'
# 2. Replace all the placeholder values with your actual LinkedIn tokens
# 3. Follow the instructions in linkedin_auth_guide.md to get your tokens

# ==========================================
# AUTHENTICATION SETTINGS - UPDATE WHEN TOKENS EXPIRE
# ==========================================

# Main authentication tokens (update these when they expire)
CSRF_TOKEN = "ajax:YOUR_CSRF_TOKEN_HERE"
JSESSIONID = "ajax:YOUR_JSESSIONID_HERE"

# LinkedIn authentication cookies (update when expired)
LI_AT_TOKEN = "YOUR_LI_AT_TOKEN_HERE"
LI_RM_TOKEN = "YOUR_LI_RM_TOKEN_HERE"

# Browser/device cookies (usually stable, but update if needed)
BCOOKIE = "YOUR_BCOOKIE_HERE"
BSCOOKIE = "YOUR_BSCOOKIE_HERE"
LIDC_COOKIE = "YOUR_LIDC_COOKIE_HERE"

# Page instance (update if you get different navigation contexts)
PAGE_INSTANCE = "urn:li:page:p_flagship3_search_srp_content;YOUR_PAGE_INSTANCE_HERE"

# GraphQL query ID (rarely changes, but update if needed)
QUERY_ID = "voyagerSearchDashClusters.YOUR_QUERY_ID_HERE" 