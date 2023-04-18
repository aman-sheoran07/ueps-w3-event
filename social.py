import os
import json
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

# Set your LinkedIn API credentials
CLIENT_ID = "77gyennvvzjh4t"
CLIENT_SECRET = "TtN6f7w363kEww7J"
ACCESS_TOKEN_URL = "https://www.linkedin.com/developers/tools/oauth/token-generator?clientId=77gyennvvzjh4t&refreshKey=1681804175746"
API_BASE_URL = "https://api.linkedin.com/v2/"

# Set the text and image for your post
POST_TEXT = "Hello, world!"
IMAGE_URL = "image.jpg"

# Authenticate with the LinkedIn API
def authenticate():
    client = BackendApplicationClient(client_id=CLIENT_ID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=ACCESS_TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return oauth

# Create a post on LinkedIn
def create_post(oauth):
    headers = {"X-Restli-Protocol-Version": "2.0.0", "Content-Type": "application/json"}
    post_data = {
        "author": "urn:li:organization:your_organization_id",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": POST_TEXT},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    if IMAGE_URL:
        post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [{"status": "READY", "originalUrl": IMAGE_URL}]
    response = oauth.post(f"{API_BASE_URL}ugcPosts", headers=headers, json=post_data)
    response_json = response.json()
    if response.status_code != 201:
        print(f"Failed to create LinkedIn post. Response: {response_json}")
    else:
        print("Successfully created LinkedIn post.")

# Authenticate with the LinkedIn API and create a post
oauth = authenticate()
create_post(oauth)
