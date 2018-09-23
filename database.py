from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import settings

connect_string = settings.DATABASE.get('url')

engine = create_engine(connect_string, pool_recycle=3600)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import User
    Base.metadata.create_all(bind=engine)
