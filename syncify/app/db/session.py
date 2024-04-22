from sqlalchemy import create_engine
from sqlalchemy import DDL
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

SQLALCHEMY_DATABASE_URI = settings.sqlalchemy_url

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with engine.connect() as connection:
    connection.execute(DDL("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))