import sys
import json
from get_profile_identifiers import get_identifiers
from linkedin_add_connection import send_connection_invite

"""
linkedin_connect_by_url.py
-------------------------
CLI wrapper: give it a LinkedIn profile URL, it resolves the necessary
identifiers and fires the connection invite via linkedin_add_connection.py.

Example:
    python linkedin_connect_by_url.py https://www.linkedin.com/in/tejaswini-yadav-05095384/
"""


def main(profile_url: str):
    print(f"🔍 Resolving identifiers for {profile_url} …")
    info = get_identifiers(profile_url)
    if not info:
        print("❌ Failed to obtain profile identifiers. Check cookies/session.")
        sys.exit(1)

    missing = [k for k in ("member_id", "profile_id", "first_name", "last_name") if not info.get(k)]
    if missing:
        print(f"❌ Missing fields: {', '.join(missing)} – cannot proceed.")
        print(json.dumps(info, indent=2))
        sys.exit(1)

    print("✅ Identifiers acquired:")
    print(json.dumps(info, indent=2))

    # Send invite
    resp = send_connection_invite(
        member_id=info["member_id"],
        profile_id=info["profile_id"],
        first_name=info["first_name"],
        last_name=info["last_name"],
        public_identifier=info["public_identifier"],
    )

    if resp.status_code == 200:
        print("🎉 Invitation request accepted by LinkedIn (HTTP 200). Check sent invites tab.")
    else:
        print(f"⚠️ LinkedIn responded with status {resp.status_code}. Inspect output above.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python linkedin_connect_by_url.py <profile_url>")
        sys.exit(1)
    main(sys.argv[1]) 