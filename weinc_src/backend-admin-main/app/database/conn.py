from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pymongo import MongoClient


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI 인스턴스
        :param kwargs:
        :return:
        """
        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", True)

        self._engine = create_engine(
            database_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )

        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            # L().info("DB connected")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            # L().info("DB disconnected")

    def get_db(self):
        """
        요청 마다 DB 세션 유지 함수
        :return:
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


class Mongo:
    def __init__(self, app: FastAPI = None, **kwargs):
        self.client = None
        self.database = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        database_url = kwargs.get("MONGO_DB_URL")
        self.client = MongoClient(database_url)
        self.database = self.client['conia-v3']

        @app.on_event("startup")
        def startup():
            print("Mongo connected")
            # L().info("Mongo connected")

        @app.on_event("shutdown")
        def shutdown():
            self.client.close()
            # L().info("Mongo disconnected")

    def collection(self, collection: str):
        col = self.database[collection]
        return col

    @property
    def api_access(self):
        return self.database["api-access"]

    @property
    def api_log(self):
        return self.database["api-log"]




db = SQLAlchemy()
Base = declarative_base()

mongo = Mongo()
