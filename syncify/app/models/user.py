from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from syncify.app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text('false'))
    is_superuser = Column(Boolean, nullable=False, server_default=text('false'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
