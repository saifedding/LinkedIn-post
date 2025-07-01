import requests
import re
import json
import uuid
import sys
from typing import Optional, Dict

"""
get_profile_identifiers.py
--------------------------
Given a LinkedIn public profile URL (e.g. https://www.linkedin.com/in/jane-doe/)
this script prints five key identifiers you can feed into
`linkedin_add_connection.py`:

1. member_id          – numeric inside urn:li:member:<id>
2. profile_id         – encoded ID inside urn:li:fsd_profile:<id>
3. first_name         – exact spelling/casing on LinkedIn
4. last_name          – exact spelling/casing on LinkedIn
5. public_identifier  – the URL slug (jane-doe)

It relies on your valid LinkedIn cookies (li_at, JSESSIONID, etc.) exactly like
other scripts in this repo.  Update the COOKIES dict below with your own
values before running.
"""

# ----------------------------
# ✨  CONFIG – fill in your own
# ----------------------------
COOKIES = {
    "li_at": "AQEDASP6v4EBfhJ7AAABl8BT3OQAAAGX5GBg5E0AocvtLBfU2unQg6KLYHNi6AG83PSJwqQdkZ2kcjhYnS0jlwh0Xy834jLziuj_Kdg3yOwz-L-QrbzlBOjMqHho03KrmOqhKNRdfYXUPajAOyj_oUg_",
    "JSESSIONID": "ajax:4763283604314235653",
    # --- keep the rest identical to your browser session or reuse the big set ---
}

HEADERS_BASE = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "csrf-token": COOKIES.get("JSESSIONID", ""),
    "accept": "application/vnd.linkedin.normalized+json+2.1",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "x-restli-protocol-version": "2.0.0",
}

SESSION = requests.Session()
SESSION.cookies.update(COOKIES)
SESSION.headers.update(HEADERS_BASE)

# Default timeout (seconds) for LinkedIn requests
TIMEOUT = 30

# Simple helper to GET with retry (handles transient connect timeouts)
def safe_get(url: str, headers: Dict, attempts: int = 3):
    """GET with basic retry on connection/read timeouts."""
    for i in range(attempts):
        try:
            return SESSION.get(url, headers=headers, timeout=TIMEOUT)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            if i == attempts - 1:
                raise
            continue


def extract_public_identifier(url: str) -> str:
    """Return the slug after /in/ from a LinkedIn profile URL."""
    if "/in/" not in url:
        return url.strip("/")
    slug = url.split("/in/")[-1]
    slug = slug.split("?")[0].split("#")[0].strip("/")
    return slug


def fetch_identity(public_id: str) -> Optional[Dict]:
    url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}"
    headers = SESSION.headers.copy()
    headers.update({
        "referer": f"https://www.linkedin.com/in/{public_id}/",
        "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{uuid.uuid4()}",
    })
    resp = safe_get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    print(f"❌ Failed to fetch identity. Status {resp.status_code}")
    return None


def sniff_member_and_name(data: Dict) -> Dict:
    member_id = None
    profile_id = None
    first_name = None
    last_name = None

    # Helper to update first/last if we find better data
    def maybe_set_name(f, l):
        nonlocal first_name, last_name
        if f and not first_name:
            first_name = f
        if l and not last_name:
            last_name = l

    # Look at main keys
    for k in ("firstName", "lastName"):
        if k in data and isinstance(data[k], str):
            if k == "firstName":
                first_name = data[k]
            else:
                last_name = data[k]

    if "objectUrn" in data and "urn:li:member:" in data["objectUrn"]:
        member_id = data["objectUrn"].split(":")[-1]

    if "entityUrn" in data and "fsd_profile" in data["entityUrn"]:
        profile_id = data["entityUrn"].split(":")[-1]

    # Scan included elements too
    for elem in data.get("included", []):
        etype = elem.get("$type", "")
        if "Profile" in etype or "MiniProfile" in etype:
            if not member_id and "objectUrn" in elem and "urn:li:member:" in elem["objectUrn"]:
                member_id = elem["objectUrn"].split(":")[-1]
            if not profile_id and "entityUrn" in elem and "fsd_profile" in elem["entityUrn"]:
                profile_id = elem["entityUrn"].split(":")[-1]
            maybe_set_name(elem.get("firstName"), elem.get("lastName"))

    return {
        "member_id": member_id,
        "profile_id": profile_id,
        "first_name": first_name,
        "last_name": last_name,
    }


def get_identifiers(profile_url: str) -> Dict:
    """Return the five identifiers for a given LinkedIn profile URL.

    Keys: member_id, profile_id, first_name, last_name, public_identifier
    """
    public_id = extract_public_identifier(profile_url)
    data = fetch_identity(public_id)
    if not data:
        return {}
    info = sniff_member_and_name(data)
    info["public_identifier"] = public_id

    # Fallback for profile_id as done in main()
    if not info.get("profile_id"):
        pv_url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/profileView"
        headers = SESSION.headers.copy()
        headers.update({
            "referer": f"https://www.linkedin.com/in/{public_id}/",
            "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{uuid.uuid4()}",
            "accept": "application/vnd.linkedin.normalized+json+2.1",
        })
        pv_resp = safe_get(pv_url, headers=headers)
        if pv_resp.status_code == 200:
            try:
                pv_json = pv_resp.json()
            except json.JSONDecodeError:
                pv_json = {}
            combined_text = json.dumps(pv_json)
            m = re.search(r"urn:li:fsd_profile:([A-Za-z0-9_-]{20,})", combined_text)
            if m:
                info["profile_id"] = m.group(1)

    return info


def main(url: str):
    public_id = extract_public_identifier(url)
    data = fetch_identity(public_id)
    if not data:
        sys.exit(1)
    info = sniff_member_and_name(data)
    info["public_identifier"] = public_id

    # Fallback: if profile_id missing, hit the /profileView endpoint and search for fsd_profile URN
    if not info.get("profile_id"):
        pv_url = f"https://www.linkedin.com/voyager/api/identity/profiles/{public_id}/profileView"
        headers = SESSION.headers.copy()
        headers.update({
            "referer": f"https://www.linkedin.com/in/{public_id}/",
            "x-li-page-instance": f"urn:li:page:d_flagship3_profile_view_base;{uuid.uuid4()}",
            "accept": "application/vnd.linkedin.normalized+json+2.1",
        })
        pv_resp = safe_get(pv_url, headers=headers)
        if pv_resp.status_code == 200:
            try:
                pv_json = pv_resp.json()
            except json.JSONDecodeError:
                pv_json = {}
            combined_text = json.dumps(pv_json)
            m = re.search(r"urn:li:fsd_profile:([A-Za-z0-9_-]{20,})", combined_text)
            if m:
                info["profile_id"] = m.group(1)
        # else ignore

    missing = [k for k, v in info.items() if not v]
    if missing:
        print("⚠️  Could not find: ", ", ".join(missing))
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_profile_identifiers.py <profile_url>")
        sys.exit(1)
    main(sys.argv[1]) 