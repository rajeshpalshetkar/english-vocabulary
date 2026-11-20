from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES=["https://www.googleapis.com/auth/blogger"]
if not Path("client_secret.json").exists(): raise SystemExit("Place the Google OAuth Desktop client JSON at client_secret.json")
flow=InstalledAppFlow.from_client_secrets_file("client_secret.json",SCOPES)
creds=flow.run_local_server(port=0,access_type="offline",prompt="consent")
print("\\nBLOGGER_REFRESH_TOKEN="+(creds.refresh_token or "NOT RETURNED"))
print("Copy this value to GitHub Secrets. Never commit it.")
