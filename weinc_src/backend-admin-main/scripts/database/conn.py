from dataclasses import asdict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pymongo import MongoClient

from app.utils.log import L
from app.common.config import conf


class SQLAlchemy:
    def __init__(self, **kwargs):
        self._engine = None
        self._session = None

        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", False)

        self._engine = create_engine(
            database_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )

        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def startup(self):
        self._engine.connect()
        L().info("DB connected")

    def shutdown(self):
        self._session.close_all()
        self._engine.dispose()
        L().info("DB disconnected")

    @property
    def session(self):
        return self._session()

    @property
    def engine(self):
        return self._engine


class Mongo:
    def __init__(self, **kwargs):
        database_url = kwargs.get("MONGO_DB_URL")
        self.client = MongoClient(database_url)
        self.database = self.client['conia-v3']

    def shutdown(self):
        self.client.close()
        # L().info("Mongo disconnected")

    def collection(self, collection: str):
        col = self.database[collection]
        return col



Base = declarative_base()
c = conf()
conf_dict = asdict(c)
db = SQLAlchemy(**conf_dict)

mongo = Mongo(**conf_dict)