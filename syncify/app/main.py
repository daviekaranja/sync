from fastapi_offline import FastAPIOffline
from starlette.middleware.sessions import SessionMiddleware

from syncify.app.api.api_v1 import api
from syncify.app.db.base import Base
from syncify.app.db.session import engine
from syncify.app.scripts import backend_prestart
from syncify.app.scripts.system_logger import logger
from syncify.app.core.middlewares import RequestLoggerMiddleware

Base.metadata.create_all(bind=engine)  # creates all tables
app = FastAPIOffline()
app.add_middleware(SessionMiddleware, secret_key='any string will do')

# routers
app.include_router(api.api_router, prefix='/api/v1/en')


@app.on_event('startup')
async def on_startup():
    backend_prestart.main()
