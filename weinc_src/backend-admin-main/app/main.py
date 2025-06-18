from dataclasses import asdict

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.common.config import conf
from app.common.open_api_docs import TAGS_METADATA
from app.database.conn import db, mongo
from app.middlewares.core import access_control
from app.middlewares.trusted_host import TrustedHostMiddleware
from app.routers import auth, permission, catalog, order, coupon, board, value, commission, dashboard, settlement, photo, menu, payment, revenue, ecoupon
from app.routers.user import company, customer, member, shop
from app.routers.product import product, brand, category, common_info, shipping_info, info, option, badge, request, qna, review
from app.routers.store import store, theme as store_theme, user as store_user, product as store_product, popup, board as store_board


def create_app():
    """
    앱 함수 실행
    :return:
    """
    c = conf()
    _app = FastAPI(
        title="Conia Platform V3 API",
        description="코니아 플랫폼 V3 API 규격 정의 문서 입니다.",
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


    # 라우터 정의
    _app.include_router(auth.router, tags=["Auth"])
    _app.include_router(member.router, tags=["Member"])
    _app.include_router(company.router, tags=["Company"])
    _app.include_router(shop.router, tags=["Company"])
    _app.include_router(permission.router, tags=["Permission"])
    _app.include_router(badge.router, tags=["Product Badge"])
    _app.include_router(brand.router, tags=["Product Brand"])
    _app.include_router(category.router, tags=["Product Category"])
    _app.include_router(common_info.router, tags=["Product Common Info"])
    _app.include_router(shipping_info.router, tags=["Product Shipping Info"])
    _app.include_router(request.router, tags=["Product Request"])
    _app.include_router(review.router, tags=["Product Review"])
    _app.include_router(qna.router, tags=["Product Qna"])
    _app.include_router(product.router, tags=["Product"])
    _app.include_router(info.router, tags=["Product Info"])
    _app.include_router(option.router, tags=["Product Option"])
    _app.include_router(commission.router, tags=["Commission"])
    _app.include_router(store.router, tags=["Store"])
    _app.include_router(store_theme.router, tags=["Store"])
    _app.include_router(store_user.router, tags=["Store"])
    _app.include_router(popup.router, tags=["Store"])
    _app.include_router(store_product.router, tags=["Store"])
    _app.include_router(store_board.router, tags=["Store"])
    _app.include_router(catalog.router, tags=["Catalog"])
    _app.include_router(order.router, tags=["Order"])
    _app.include_router(coupon.router, tags=["Coupon"])
    _app.include_router(board.router, tags=["Board"])
    _app.include_router(value.router, tags=["Value"])
    _app.include_router(dashboard.router, tags=["DashBoard"])
    _app.include_router(customer.router, tags=["Customer"])
    _app.include_router(settlement.router, tags=["Settlement"])
    _app.include_router(photo.router, tags=["Photo"])
    _app.include_router(menu.router, tags=["Menu"])
    _app.include_router(payment.router, tags=["Payment"])
    _app.include_router(revenue.router, tags=["Revenue"])
    _app.include_router(ecoupon.router, tags=["Ecoupon"])

    return _app


app = create_app()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
