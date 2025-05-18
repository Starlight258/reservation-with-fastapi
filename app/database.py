from sqlmodel import SQLModel, create_engine, Session

from app.config import SQLITE_URL, DATABASE_CONNECT_ARGS

engine = create_engine(SQLITE_URL, connect_args=DATABASE_CONNECT_ARGS)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session 