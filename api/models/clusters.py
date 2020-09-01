"""This module defines the database structure for the application"""
from dataclasses import dataclass
from sqlalchemy import Column, String, ForeignKey
from api.database import BaseModel, GUID


@dataclass
class Cluster(BaseModel):
    """This class sets up a table for user accounts"""
    __tablename__ = "clusters"
    user_uuid: str # noqa
    mac_address: str
    ip_address: str
    status: str
    version: str

    user_uuid = Column(GUID(), ForeignKey('users.uuid'))
    mac_address = Column(String, unique=True, nullable=False)
    ip_address = Column(String, nullable=False)
    status = Column(String, nullable=False)
    version = Column(String, nullable=False)

    def __init__(self, user_uuid=None, mac_address=None,
                 ip_address=None, status=None, version=None):
        """Sets a default of member for a users role unless otherwise
        specified"""
        self.user_uuid = user_uuid
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.status = status
        self.version = version
