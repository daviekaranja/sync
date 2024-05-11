from authlib.integrations.starlette_client import OAuth, OAuthError
from syncify.app.core.config import settings

oauth = OAuth()

oauth.register(
    name='facebook',
    client_id=settings.facebook_id,
    client_secret=settings.facebook_secret,
    authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
    authorize_params=None,
    access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    refresh_token_params=None,
    client_kwargs={'scope': 'email'},
)
