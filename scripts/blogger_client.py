import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
SCOPES=["https://www.googleapis.com/auth/blogger"]
def service():
 keys=["BLOGGER_CLIENT_ID","BLOGGER_CLIENT_SECRET","BLOGGER_REFRESH_TOKEN","BLOGGER_BLOG_ID"]
 missing=[k for k in keys if not os.getenv(k)]
 if missing: raise RuntimeError("Missing GitHub secrets: "+", ".join(missing))
 c=Credentials(token=None,refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],token_uri="https://oauth2.googleapis.com/token",client_id=os.environ["BLOGGER_CLIENT_ID"],client_secret=os.environ["BLOGGER_CLIENT_SECRET"],scopes=SCOPES)
 c.refresh(Request())
 return build("blogger","v3",credentials=c,cache_discovery=False)
def blog_id(): return os.environ["BLOGGER_BLOG_ID"]
