from authlib.integrations.starlette_client import OAuth, OAuthError

oauth = OAuth()

oauth.register(
    name='facebook'
)