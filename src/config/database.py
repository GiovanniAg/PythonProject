from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, Engine

from config.env import env

class Base(DeclarativeBase):
    pass

engine: Engine = create_engine(
    url=f"postgresql+psycopg2://{env.db_user}:{env.db_pass}@{env.db_host}:{env.db_port}/{env.db_name}"
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)