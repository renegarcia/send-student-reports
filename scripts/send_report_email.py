import msal
import requests
import time
import os


def setup_access_token():
    client_id = os.environ["CLIENT_ID"]
    tenant_id = "consumers"
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["Mail.Send"]
    # Create a public client app (delegated flow)
    app = msal.PublicClientApplication(
        client_id,
        authority=authority,
    )

    result = app.acquire_token_interactive(scopes=scope)

    if "access_token" in result:
        token = result["access_token"]
        return token
    else:
        raise Exception("Failed to obtain token: ", result.get("error"))


def send_report_email(recipient, subject, html_content, token, retries=3):
    endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
    email_msg = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": html_content},
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        },
        "saveToSentItems": "true",
    }
    for attempt in range(retries):
        response = requests.post(
            endpoint,
            headers={"Authorization": f"Bearer {token}"},
            json=email_msg,
        )
        if response.status_code == 202:
            print(f"✅ Email sent to {recipient}")
            return True
        elif response.status_code == 429:  # throttled
            retry_after = int(response.headers.get("Retry-After", "5"))
            print(f"⚠️ Throttled. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"❌ Error {response.status_code} for {recipient}: {response.text}")
            time.sleep(2**attempt)  # exponential backoff
        return False
