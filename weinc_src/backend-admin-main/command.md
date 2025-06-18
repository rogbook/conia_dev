# 명령어

* JWT secret key 생성
  * `openssl rand -hex 32`
---
* SQLAlchemy 모델 파일 생성
  * `pip install sqlacodegen`
  * `sqlacodegen "mysql+pymysql://user:password@localhost/dbname" > sqlalchemy_models.py`
