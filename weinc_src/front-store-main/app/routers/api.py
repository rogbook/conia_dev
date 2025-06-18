from fastapi import APIRouter
from app.routers.apis import store, board, cart, order, auth, product, wish, customer
from app.models.product import DataProduct
from datetime import datetime

router = APIRouter(prefix="/api")

router.include_router(auth.router, tags=["Auth"])
router.include_router(customer.router, tags=["Customer"])
router.include_router(product.router, tags=["Product"])
router.include_router(store.router, tags=["Store"])
router.include_router(cart.router, tags=["Cart"])
router.include_router(wish.router, tags=["Wish"])
router.include_router(order.router, tags=["Order"])
router.include_router(board.router, tags=["Board"])

@router.get("/dummy-product", response_model=DataProduct)
async def get_dummy_product():
    return DataProduct(
        id=1,
        member_id=1,
        name="테스트 상품",
        type="normal",
        status="active",
        view_yn="Y",
        code="P001",
        summary="테스트용 상품입니다.",
        keyword="테스트,상품",
        contents="이것은 테스트 상품의 상세 설명입니다.",
        tax="Y",
        min_purchase_limit=1,
        max_purchase_limit=10,
        adult="N",
        hscode=None,
        reg_date=datetime.now(),
        mod_date=datetime.now(),
        ipcc_yn="N",
        cancel_yn="N",
        confirm="Y",
        video=None,
        memo=None,
        common_info_id=None,
        shipping_info_id=None,
        inven_use="Y",
        coupon_yn="N",
        option_use="N",
        barcode=None,
        user_limit=None,
        use_end_period=None,
        use_end_date=None,
        sale_start_date=None,
        sale_end_date=None,
        sale_start_time=None,
        sale_end_time=None,
        tel=None,
        address=None,
        lat=None,
        lng=None,
        subtitle=None,
        view_inventory=None,
        view_end_time=None,
        api_provider=None,
        api_goods_id=None,
        use_place=None,
        user_limit_reset=None,
        inven_cnt=100,
        is_sold_out=False,
        product_default=None,
        common_info=None,
        options=None,
        photos=[],
        reviews=None,
        badges=None,
        brands=None
    )
