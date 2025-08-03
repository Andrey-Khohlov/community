import urllib.parse
import secrets

# from state_storage import state_storage
from app.config import settings


def generate_google_oauth_redirect_uri():
    # random_state = secrets.token_urlsafe(16)
    # state_storage.add(random_state)

    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": "http://localhost:8550/v1/auth/google",
        "response_type": "code",
        "scope": " ".join([
            "openid",
            "profile",
            "email",
        ]),
        # "state": random_state,
    }

    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    print(f"{base_url}?{query_string}")
    return f"{base_url}?{query_string}"