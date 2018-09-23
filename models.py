from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, String, text, Boolean, Enum, Text, SmallInteger, Date
from sqlalchemy.orm import relationship
from database import Base, db_session
import uuid, datetime, settings

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()) )
    username = Column(Text(), nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    name = Column(Text(), nullable=True)
    status = Column(Boolean , nullable=False, server_default=text("1"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def __init__(self, username = None, password=None,  email = None, name = None):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.created_at =datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.username)


class Session(Base):
    __tablename__ = 'user_sessions'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    token = Column(String(255), nullable=True)
    token_expiration = Column(DateTime, default=datetime.datetime.utcnow)
    ip = Column(String(50), nullable=True)
    browser = Column(Text(), nullable=True)
    user_id = Column(ForeignKey(u'users.id'), nullable=False, index=True)

    user = relationship(u'User')

    def __init__(self, user_id= None, token= None, ip= None, browser= None):
        self.user_id = user_id
        self.token = token
        self.token_expiration =  datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.SESSION.get('token_expiration'))
        self.ip = ip
        self.browser = browser

    def __repr__(self):
        return '<Session %r>' % (self.id)
