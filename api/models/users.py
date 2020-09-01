"""This module defines the database structure for the application"""
from dataclasses import dataclass
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import sha256_crypt
from api.database import BaseModel, GUID
from api.models.clusters import Cluster


@dataclass
class User(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "users"
    username: str # noqa
    role: str

    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    api_keys = relationship('Tokens', backref='user', lazy=True)
    clusters = relationship('Cluster', backref='user', lazy=True)

    def __init__(self, username=None, password=None, role='member'):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.username = username
        self.password_hash = sha256_crypt.hash(password)
        self.role = role

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password_hash)

    def __repr__(self):
        """Return the username"""
        return '<User %r>' % self.username


@dataclass
class Tokens(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "tokens"
    api_key: str # noqa
    revoked: bool

    user_uuid = Column(GUID(), ForeignKey('users.uuid'))
    revoked = Column(Boolean, nullable=False)
    api_key = Column(String, unique=True, nullable=False)

    def __init__(self, user_uuid=None, revoked=False, api_key=None):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.user_uuid = user_uuid
        self.revoked = revoked
        self.api_key = api_key


@dataclass
class PacketTokens(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "packettokens"
    api_key: str # noqa
    revoked: bool

    user_uuid = Column(GUID(), ForeignKey('users.uuid'))
    revoked = Column(Boolean, nullable=False)
    api_key = Column(String, unique=True, nullable=False)

    def __init__(self, user_uuid=None, revoked=False, api_key=None):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.user_uuid = user_uuid
        self.revoked = revoked
        self.api_key = api_key
