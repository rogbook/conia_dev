import os
from pathlib import Path
from dataclasses import asdict

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.common.config import conf
from app.common.open_api_docs import TAGS_METADATA
from app.errors import exceptions
from app.database.conn import db, mongo
from app.middlewares.core import access_control
from app.middlewares.trusted_host import TrustedHostMiddleware
from app.routers import api, view, sns

from app.utils import fastapi_jinja


def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    _app = FastAPI(
        title="Conia Platform V3 상점용 API",
        description="코니아 플랫폼 V3 상점용 API 규격 정의 문서 입니다.",
        version="0.0.1",
        contact={
            "name": "이승준",
            "email": "yoire7@gmail.com",
        },
        openapi_tags=TAGS_METADATA
    )
    conf_dict = asdict(c)
    db.init_app(_app, **conf_dict)
    mongo.init_app(_app, **conf_dict)

    # 레디스 이니셜라이즈
    redis = aioredis.from_url(c.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="conia-cache")

    # 미들웨어 정의
    _app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(TrustedHostMiddleware, allowed_hosts=conf().TRUSTED_HOSTS, except_path=[""])

    # Rate Limit 처리

    # 템플릿 리소스 폴더 정의
    folder = os.path.dirname(__file__)
    template_folder = os.path.join(folder, "templates")
    fastapi_jinja.global_init(template_folder)

    current_file = Path(__file__)
    current_file_dir = current_file.parent
    project_root = current_file_dir.parent
    project_root_absolute = project_root.resolve()
    static_root_absolute = project_root_absolute / "app/static/dist"
    _app.mount("/static/dist", StaticFiles(directory=static_root_absolute), name="static")

    # 라우터 정의
    _app.include_router(api.router)
    _app.include_router(sns.router)
    _app.include_router(view.router, prefix="/{store_code}")

    @_app.get("/")
    def index():
        return RedirectResponse(url="https://coniaworld.com")

    return _app


app = create_app()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8082, reload=True)
