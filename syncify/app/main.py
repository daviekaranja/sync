from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi_offline import FastAPIOffline
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader

from syncify.app.api.api_v1 import api
from syncify.app.db.base import Base
from syncify.app.db.session import engine
from syncify.app.scripts import backend_prestart
from syncify.app.api import dependancies
from .core.config import settings
from syncify.app.scripts.system_logger import logger
from .core.middlewares import check_authentication
from syncify.app.core.middlewares import RequestLoggerMiddleware

env = Environment(loader=FileSystemLoader(searchpath=settings.staticfiles))
Base.metadata.create_all(bind=engine)  # creates all tables
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# routers
app.include_router(api.api_router, prefix='/api')


@app.on_event('startup')
async def on_startup():
    backend_prestart.main()


@app.get('/check', status_code=200)
async def health():
    return 'Welcome'


@app.get('/', status_code=200)
def home():
    template = env.get_template('home.html')
    context = {
        'title': "SocialSync",
        'name': 'User'
    }
    output = template.render(context)
    return HTMLResponse(output)


@app.get('/docs', status_code=200)
def documentation(request: Request):
    user = request.session.get('user')
    if user is None:
        raise HTTPException(status_code=401, detail='Not Authorized')
    logger.info(user['is_active'])
