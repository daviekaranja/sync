import secrets
from ..core.config import settings

from authlib.integrations.starlette_client import OAuth, OAuthError

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    access_token_url="https://www.googleapis.com/oauth2/v4/token",
    api_base_url="https://www.googleapis.com/",
    scope="profile email openid",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
    # Google's OpenID Connect metadata
)


