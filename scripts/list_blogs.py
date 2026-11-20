import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
c=Credentials(token=None,refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],token_uri="https://oauth2.googleapis.com/token",client_id=os.environ["BLOGGER_CLIENT_ID"],client_secret=os.environ["BLOGGER_CLIENT_SECRET"],scopes=["https://www.googleapis.com/auth/blogger"])
c.refresh(Request()); api=build("blogger","v3",credentials=c,cache_discovery=False)
for b in api.blogs().listByUser(userId="self").execute().get("items",[]):
 print(f'{b.get("name")} | ID: {b.get("id")} | {b.get("url")}')
