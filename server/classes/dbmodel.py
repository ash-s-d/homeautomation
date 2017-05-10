"""dbmodel.py: Partially generated SQLAlchemy data model code, from the existing SQLite database, via the sqlacodegen tool"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"

Base = declarative_base()

metadata = Base.metadata


class Camera(Base):
    __tablename__ = 'Camera'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128))
    mac_address = Column(String(17), nullable=False, unique=True)
    ip_address = Column(String(15))

    zones = relationship(u'Zone', secondary='Zone_Camera')


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    login = Column(Unicode(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    full_name = Column(Unicode(256), nullable=False)


class WifiBridge(Base):
    __tablename__ = 'WifiBridge'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(256))
    mac_address = Column(String(17), nullable=False, unique=True)
    ip_address = Column(String(15))

    zones = relationship(u'Zone', secondary='Zone_WifiBridge')


class Zone(Base):
    __tablename__ = 'Zone'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128), nullable=False, unique=True)
    description = Column(Unicode(256), nullable=False)


t_Zone_Camera = Table(
    'Zone_Camera', metadata,
    Column('zone_id', ForeignKey(u'Zone.id'),
           primary_key=True, nullable=False),
    Column('camera_id', ForeignKey(u'Camera.id'),
           primary_key=True, nullable=False)
)


t_Zone_WifiBridge = Table(
    'Zone_WifiBridge', metadata,
    Column('zone_id', ForeignKey(u'Zone.id'),
           primary_key=True, nullable=False),
    Column('wifi_bridge_id', ForeignKey(u'WifiBridge.id'),
           primary_key=True, nullable=False)
)
