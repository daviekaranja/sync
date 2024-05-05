from fastapi import FastAPI
from fastapi_offline import FastAPIOffline
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse

from syncify.app.api.api_v1 import api
from syncify.app.db.base import Base
from syncify.app.db.session import engine
from syncify.app.scripts import backend_prestart
from .core.config import settings
from syncify.app.scripts.system_logger import logger
from syncify.app.core.middlewares import RequestLoggerMiddleware

Base.metadata.create_all(bind=engine)  # creates all tables
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# routers
app.include_router(api.api_router, prefix='/api')


@app.on_event('startup')
async def on_startup():
    backend_prestart.main()


@app.get('/', status_code=200)
def home():
    html_response = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        /* Style for the login card */
        .login-card {
            width: 300px;
            margin: auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        /* Style for the login button */
        .login-button {
            display: block;
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            background-color: #4285f4;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
        }

        .login-button:hover {
            background-color: #357ae8;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>Login</h2>
        <!-- "Login with Google" button -->
        <a href="/api/auth/login/google" class="login-button">Login with Google</a>
    </div>
</body>
</html>

    """
    return HTMLResponse(html_response)
