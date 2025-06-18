from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Legacy:
    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:j<Am33?rlT:R09cS@211.110.209.71:16033/CONIA_V2?charset=utf8mb4",
            echo=True,
            pool_recycle=900,
            pool_pre_ping=True,
        )

        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.engine.connect()

    def execute(self, qry: str):
        return self.session().execute(text(qry))

    def close(self):
        self.session.close_all()
        self.engine.dispose()
