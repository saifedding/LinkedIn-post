import requests
import json
import argparse

"""
This script recreates the PowerShell Invoke-WebRequest sample in Python.
It establishes a requests.Session(), adds the same cookies and headers, and
performs the POST request to send a LinkedIn connection invitation via the
flagship RSC action endpoint.

⚠️  WARNING
---------------------------------------------
Running this script with the hard-coded cookies below will only succeed if the
cookies are still valid *for your own LinkedIn account*.  Treat these
credentials as secrets: never commit them to a public repo and rotate them when
possible.  Prefer loading them from environment variables or a secure vault in
real usage.
"""

# ------------------------------------------------------
# 1.  Define all cookies exactly as in the PowerShell demo
# ------------------------------------------------------
COOKIES = {
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
    "AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg": "1",
    "AMCV_14215E3D5995C57C0A495C55%40AdobeOrg": "-637568504%7CMCIDTS%7C20270%7CMCMID%7C27573806750435840703114589459359274076%7CMCOPTOUT-1751285608s%7CNONE%7CvVersion%7C5.1.1",
    "g_state": "{\"i_l\":0}",
    "liap": "true",
    "li_at": "AQEDASP6v4EBfhJ7AAABl8BT3OQAAAGX5GBg5E0AocvtLBfU2unQg6KLYHNi6AG83PSJwqQdkZ2kcjhYnS0jlwh0Xy834jLziuj_Kdg3yOwz-L-QrbzlBOjMqHho03KrmOqhKNRdfYXUPajAOyj_oUg_",
    "fptctx2": "taBcrIH61PuCVH7eNCyH0I1otfYAPn9VOPY9aMX8tO1OZsqBMQoiv4L3v0T63VjmZLQa16kvaMUYVUosFXHHtS3l3aC7%252bp1EFIAkHKyNtQRBhoos8j9BfdkViImt83dvAFqcppQGcz5heoO6EHiT%252f4%252fo0q8d5J%252fVxUZEp96Us7VIOyOM%252bmSTLpH2i1y8oeEVtcpfBmLwYDde1Yob93OmmIMk8sM6ls6fTQuIV6wRxPhjhbqreXRNfNF65F%252fsef3sfHiGDiiVSmW5NhYn4REDR9M%252b80Ie9UZfBerOWGnqyXiWH2S18PeEyCH%252be7vOVIfZNPbVFIcT%252biOr3NnQHE7grh%252fUHmoqJl7PFDOB8OB5OHI%253d",
    "UserMatchHistory": "AQI7Ds3eSZVbMAAAAZfFxlLaOPowaiDZIYW-cxr3OPK4Qvw_bXY1A7iGrGiHLlIAdi2VKhKp1aEMTmOqLKD_pt8GPRNqo3hoxYHwik6cRfGoZuCBwhw9a_NT6fq8_3KCn1cR3ecfX2beF6l9VW921VO0S16xr4vRGp7NHsXwgiNAOad47PpqwBTSs1JfveNGw8DpLttEKYNhhDnrF7UQj4UxhTxL_nQmoqSNyZb5mmPWDWyXt9_chDuRL1mBuOzz5DjApAOMt_iP6m1Zsd5U7M5QGDOG-9BDoJsDtjdbD1KOXLTgMcH0pitqCRPTyhp5rdo2plmcClChMyhdgFJGqc9_QME0EhryKFpaOh8znGwCLGEYnw",
    "lidc": "b=VB85:s=V:r=V:a=V:p=V:g=5950:u=788:x=1:i=1751377346:t=1751463746:v=2:sig=AQFi7RAyUFQm32WfuBkF17CN0YPpraHh",
}

# ------------------------------------------------------
# 2.  Static headers from the Invoke-WebRequest example
# ------------------------------------------------------
HEADERS = {
    "authority": "www.linkedin.com",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "csrf-token": "ajax:4763283604314235653",
    "origin": "https://www.linkedin.com",
    "priority": "u=1, i",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-li-anchor-page-key": "d_flagship3_people",
    "x-li-application-instance": "Mrhk05/ZTo6GHeHlI64inw==",
    "x-li-application-version": "0.2.1509",
    "x-li-page-instance": "urn:li:page:d_flagship3_people;HnJ2JcZbTtWquONuu7sorg==",
    "x-li-page-instance-tracking-id": "HnJ2JcZbTtWquONuu7sorg==",
    "x-li-pageforestid": "eca9900caa90cef762b225d704d1f870",
    "x-li-traceparent": "00-eca9900caa90cef762b225d704d1f870-a4a82440ab2d9568-00",
    "x-li-tracestate": "LinkedIn=a4a82440ab2d9568",
    "content-type": "application/json",
    # The elaborate x-li-track header is easier to build via json.dumps
}

# x-li-track is a JSON-encoded header value.
HEADERS["x-li-track"] = json.dumps({
    "clientVersion": "0.2.1509",
    "mpVersion": "0.2.1509",
    "osName": "web",
    "timezoneOffset": 4,
    "timezone": "Asia/Dubai",
    "deviceFormFactor": "DESKTOP",
    "mpName": "web",
    "displayDensity": 2.5,
    "displayWidth": 3840,
    "displayHeight": 2400,
})

# User-Agent lives on the Session object so requests will send it automatically.
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

# ------------------------------------------------------
# 3.  Define request URL and JSON body
# ------------------------------------------------------
URL = (
    "https://www.linkedin.com/flagship-web/rsc-action/actions/server-request"
    "?sduiid=com.linkedin.sdui.requests.mynetwork.addaAddConnection"
)

# IMPORTANT:  The JSON payload copied from the PowerShell snippet contains a
# lot of proto namespaces and long base64 strings.  To keep this example
# readable we store it as a multi-line raw string.  No processing is performed –
# it will be sent verbatim.
#
# ⚠️  If you need to tweak fields (e.g. different profile ID) consider loading
# the JSON into a Python dict via json.loads() and editing programmatically.
JSON_BODY_RAW = r"""
{"requestId":"com.linkedin.sdui.requests.mynetwork.addaAddConnection","serverRequest":{"$type":"proto.sdui.actions.core.ServerRequest","requestId":"com.linkedin.sdui.requests.mynetwork.addaAddConnection","requestedArguments":{"$type":"proto.sdui.actions.requests.RequestedArguments","payload":{"inviteeUrn":{"memberId":"959438703"},"nonIterableProfileId":"ACoAADkv328BVRbCzCrXH8YGMhJQVLycHNUteI4","renderMode":"IconAndText","firstName":"Rahul","lastName":"Kaushal","isDisabled":{"key":"connect-button-disabled-rahul-kaushal-893392229","namespace":null},"connectionState":{"key":"state:invitation:urn:li:member:959438703","namespace":null},"origin":"InvitationOrigin_PYMK_COHORT_SECTION","profileCanonicalUrl":"https://www.linkedin.com/in/rahul-kaushal-893392229","profilePictureRenderPayload":"AApVaHR0cHM6Ly9tZWRpYS5saWNkbi5jb20vZG1zL2ltYWdlL3YyL0Q0RDAzQVFGdjY2ei1sOHVYeEEvcHJvZmlsZS1kaXNwbGF5cGhvdG8tc2hyaW5rXxJxCMgBEMgBGmkyMDBfMjAwL0I0RFpYUlNPTldIQUFZLS8wLzE3NDI5NzI5NzA3OTE/ZT0xNzU2OTQ0MDAwJnY9YmV0YSZ0PTBoZ2wyTF9ONE5BRVB3TUNaa3JHZTFWMXNZT1VYUmEyWU5pR3lDQzZlNGcScQiQAxCQAxppNDAwXzQwMC9CNERaWFJTT05XSEFBZy0vMC8xNzQyOTcyOTcwNzkxP2U9MTc1Njk0NDAwMCZ2PWJldGEmdD12S043d3NtTl9WR1ZES0VRSDZEcHpqU0ptNHJVdko3Y215OG9FeFpYRVcwEm8IZBBkGmkxMDBfMTAwL0I0RFpYUlNPTldIQUFVLS8wLzE3NDI5NzI5NzA3OTE/ZT0xNzU2OTQ0MDAwJnY9YmV0YSZ0PUhLWmxjMEc5Yndkc0F0bGVBMVo4SGI4WUtRNDd1R2RybVI2MWU2VUxYbWcScQigBhCgBhppODAwXzgwMC9CNERaWFJTT05XSEFBYy0vMC8xNzQyOTcyOTcwODQ0P2U9MTc1Njk0NDAwMCZ2PWJldGEmdD00VVRLYVA5QTVUdlBTS2RlNlVsZzRfWGV3U0lrV3dKSVdCUFh2NzJYNmJZIix1cm46bGk6ZGlnaXRhbG1lZGlhQXNzZXQ6RDREMDNBUUZ2NjZ6LWw4dVh4QQ==","firstFiveInviteCount":{"key":"guidedFlowNumSentInvites","namespace":""},"guidedFlowUrlandProfileList":{"key":"guidedFlowUrlAndPictureList","namespace":"guidedFlowUrlAndPictureListNameSpace"},"postActionSentConfigs":[]},"requestedStateKeys":[{"$type":"proto.sdui.StateKey","value":"guidedFlowNumSentInvites","key":{"$type":"proto.sdui.Key","value":{"$case":"id","id":"guidedFlowNumSentInvites"}},"namespace":""},{"$type":"proto.sdui.StateKey","value":"guidedFlowUrlAndPictureList","key":{"$type":"proto.sdui.Key","value":{"$case":"id","id":"guidedFlowUrlAndPictureList"}},"namespace":"guidedFlowUrlAndPictureListNameSpace"}],"requestMetadata":{"$type":"proto.sdui.common.RequestMetadata"}},"onClientRequestFailureAction":{"actions":[{"$type":"proto.sdui.actions.core.SetState","value":{"$type":"proto.sdui.actions.core.SetState","stateKey":"","stateValue":"","state":{"$type":"proto.sdui.State","stateKey":"","key":{"$type":"proto.sdui.StateKey","value":"state:invitation:urn:li:member:959438703","key":{"$type":"proto.sdui.Key","value":{"$case":"id","id":"state:invitation:urn:li:member:959438703"}},"namespace":""},"value":{"$case":"stringValue","stringValue":"Connect"},"isOptimistic":false},"isOptimistic":false}},{"$type":"proto.sdui.actions.core.SetState","value":{"$type":"proto.sdui.actions.core.SetState","stateKey":"","stateValue":"","state":{"$type":"proto.sdui.State","stateKey":"","key":{"$type":"proto.sdui.StateKey","value":"connect-button-disabled-rahul-kaushal-893392229","key":{"$type":"proto.sdui.Key","value":{"$case":"id","id":"connect-button-disabled-rahul-kaushal-893392229"}},"namespace":""},"value":{"$case":"booleanValue","booleanValue":false},"isOptimistic":false},"isOptimistic":false}}]},"isStreaming":false,"rumPageKey":""},"states":[],"requestedArguments":{"$type":"proto.sdui.actions.requests.RequestedArguments","payload":{"inviteeUrn":{"memberId":"959438703"},"nonIterableProfileId":"ACoAADkv328BVRbCzCrXH8YGMhJQVLycHNUteI4","renderMode":"IconAndText","firstName":"Rahul","lastName":"Kaushal","isDisabled":{"key":"connect-button-disabled-rahul-kaushal-893392229","namespace":null},"connectionState":{"key":"state:invitation:urn:li:member:959438703","namespace":null},"origin":"InvitationOrigin_PYMK_COHORT_SECTION","profileCanonicalUrl":"https://www.linkedin.com/in/rahul-kaushal-893392229","profilePictureRenderPayload":"AApVaHR0cHM6Ly9tZWRpYS5saWNkbi5jb20vZG1zL2ltYWdlL3YyL0Q0RDAzQVFGdjY2ei1sOHVYeEEvcHJvZmlsZS1kaXNwbGF5cGhvdG8tc2hyaW5rXxJxCMgBEMgBGmkyMDBfMjAwL0I0RFpYUlNPTldIQUFZLS8wLzE3NDI5NzI5NzA3OTE/ZT0xNzU2OTQ0MDAwJnY9YmV0YSZ0PTBoZ2wyTF9ONE5BRVB3TUNaa3JHZTFWMXNZT1VYUmEyWU5pR3lDQzZlNGcScQiQAxCQAxppNDAwXzQwMC9CNERaWFJTT05XSEFBZy0vMC8xNzQyOTcyOTcwNzkxP2U9MTc1Njk0NDAwMCZ2PWJldGEmdD12S043d3NtTl9WR1ZES0VRSDZEcHpqU0ptNHJVdko3Y215OG9FeFpYRVcwEm8IZBBkGmkxMDBfMTAwL0I0RFpYUlNPTldIQUFVLS8wLzE3NDI5NzI5NzA3OTE/ZT0xNzU2OTQ0MDAwJnY9YmV0YSZ0PUhLWmxjMEc5Yndkc0F0bGVBMVo4SGI4WUtRNDd1R2RybVI2MWU2VUxYbWcScQigBhCgBhppODAwXzgwMC9CNERaWFJTT05XSEFBYy0vMC8xNzQyOTcyOTcwODQ0P2U9MTc1Njk0NDAwMCZ2PWJldGEmdD00VVRLYVA5QTVUdlBTS2RlNlVsZzRfWGV3U0lrV3dKSVdCUFh2NzJYNmJZIix1cm46bGk6ZGlnaXRhbG1lZGlhQXNzZXQ6RDREMDNBUUZ2NjZ6LWw4dVh4QQ==","firstFiveInviteCount":{"key":"guidedFlowNumSentInvites","namespace":""},"guidedFlowUrlandProfileList":{"key":"guidedFlowUrlAndPictureList","namespace":"guidedFlowUrlAndPictureListNameSpace"},"postActionSentConfigs":[]},"requestedStateKeys":[{"$type":"proto.sdui.StateKey","value":"guidedFlowNumSentInvites","key":{"$type":"proto.sdui.Key","value":{"$case":"id","id":"guidedFlowNumSentInvites"}},"namespace":""},{"$type":"proto.sdui.StateKey","value":"guidedFlowUrlAndPictureList","key":{"$type":"proto.sdui.Key","value":{"$case":"id","id":"guidedFlowUrlAndPictureList"}},"namespace":"guidedFlowUrlAndPictureListNameSpace"}],"requestMetadata":{"$type":"proto.sdui.common.RequestMetadata"},"states":[]}}
"""

# ------------------------------------------------------
# Helper to mutate the base payload with new profile data
# ------------------------------------------------------

def build_payload(member_id: str, profile_id: str, first_name: str, last_name: str, public_identifier: str) -> str:
    """Return a JSON string ready to POST for a connection invite.

    This clones the static JSON template then rewrites only the
    user-dependent fields so it works for any profile.
    """

    base = json.loads(JSON_BODY_RAW)

    def _patch_requested_arguments(arg_obj: dict):
        payload_obj = arg_obj.get("payload", {})

        # Basic identity fields
        payload_obj["inviteeUrn"]["memberId"] = member_id
        payload_obj["nonIterableProfileId"] = profile_id
        payload_obj["firstName"] = first_name
        payload_obj["lastName"] = last_name
        payload_obj["profileCanonicalUrl"] = f"https://www.linkedin.com/in/{public_identifier}"

        # Dynamic keys that reference profile slug / ID
        payload_obj["isDisabled"]["key"] = f"connect-button-disabled-{public_identifier}"
        payload_obj["connectionState"]["key"] = f"state:invitation:urn:li:member:{member_id}"

    # Patch the two parallel RequestedArguments blocks
    _patch_requested_arguments(base["serverRequest"]["requestedArguments"])
    _patch_requested_arguments(base["requestedArguments"])

    # Patch failure-action state keys so UI reverts correctly on client error
    for action in (
        base["serverRequest"].get("onClientRequestFailureAction", {}).get("actions", [])
    ):
        try:
            state_val = action["value"]["state"]["key"]["value"]
            if state_val.startswith("state:invitation:urn:li:member:"):
                action["value"]["state"]["key"]["value"] = (
                    f"state:invitation:urn:li:member:{member_id}"
                )
            elif state_val.startswith("connect-button-disabled-"):
                action["value"]["state"]["key"]["value"] = (
                    f"connect-button-disabled-{public_identifier}"
                )
        except (KeyError, TypeError):
            continue

    return json.dumps(base, separators=(",", ":"))

# ------------------------------------------------------
# 4.  Fire the request (now parameterised)
# ------------------------------------------------------

def send_connection_invite(member_id: str, profile_id: str, first_name: str, last_name: str, public_identifier: str):
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    session.cookies.update(COOKIES)

    json_body = build_payload(
        member_id=member_id,
        profile_id=profile_id,
        first_name=first_name,
        last_name=last_name,
        public_identifier=public_identifier,
    )

    print(f"[+] Sending invite to {first_name} {last_name} (memberId={member_id}) ...")
    resp = session.post(URL, headers=HEADERS, data=json_body.encode("utf-8"), timeout=30)

    print(f"[+] Response status : {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2)[:2000])  # truncate large output
    except ValueError:
        print(resp.text[:2000])

    return resp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send LinkedIn connection invite through private RSC endpoint")
    parser.add_argument("member_id", help="Numeric LinkedIn member ID, e.g. 390720085")
    parser.add_argument("profile_id", help="Encoded profile ID, e.g. ACoAABdJ6lUBwgPnr8RuTqvysc3BSNfn8TrElAY")
    parser.add_argument("first_name", help="Profile first name")
    parser.add_argument("last_name", help="Profile last name")
    parser.add_argument("public_identifier", help="Public profile slug, e.g. omar-soufeh")

    args = parser.parse_args()

    send_connection_invite(
        member_id=args.member_id,
        profile_id=args.profile_id,
        first_name=args.first_name,
        last_name=args.last_name,
        public_identifier=args.public_identifier,
    ) 