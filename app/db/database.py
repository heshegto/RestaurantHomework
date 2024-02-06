# import os
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<database_name>"
# SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}/{}'.format(
#     os.getenv('POSTGRES_DB_USER', 'postgres'),
#     os.getenv('POSTGRES_DB_PASSWORD', ''),
#     os.getenv('POSTGRES_DB_CONTAINER_NAME', 'postgres'),
#     os.getenv('POSTGRES_DB', 'postgres')
# )
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:5875@localhost:5432/postgres'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
