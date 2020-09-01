"""This module configures the application to talk with a database"""
from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime
from dataclasses import dataclass
import uuid
from api.config import config


DB = config.SQLALCHEMY_DATABASE_URI

engine = create_engine(DB, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db(self):
    '''import all modules here that might define models so that
          they will be registered properly on the metadata.  Otherwise
          you will have to import them first before calling init_db()'''
    import api.models # noqa
    Base.metadata.create_all(bind=engine)


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


@dataclass
class BaseModel(Base):

    __abstract__ = True
    uuid: str
    created_at: datetime
    updated_at: datetime

    uuid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(),
                        onupdate=func.current_timestamp())
