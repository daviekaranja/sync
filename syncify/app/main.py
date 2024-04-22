from fastapi import FastAPI
from syncify.app.db.base import Base
from syncify.app.db.session import engine
from syncify.app.scripts import backend_prestart
from syncify.app.api.api_v1 import api

Base.metadata.create_all(bind=engine)  # creates all tables
app = FastAPI()
# routers
app.include_router(api.api_router, prefix='/api/v1/en')


@app.on_event('startup')
async def on_startup():
    backend_prestart.main()


@app.get('/', status_code=200)
def home():
    return 'Welcome to syncify'
