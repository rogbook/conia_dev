from typing import List
from base64 import b64decode
from urllib.parse import unquote

from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.conn import db
from app.database.schema import Store, Product, StoreProduct, ProductCategory, WishProduct, ProductOption, ShippingCost, NoticeInfo, Shop, ExtraInfo, ProductReview, ProductStoreMemo
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.product import DataProduct
from app.utils.common_utils import check_store, make_view_context_data, qry_sorter, get_ip, wish_and_product_check, get_target_store_code, cost_variation, check_sold_out
from app.utils.jwt import token_user_option, token_user
from app.utils.log import analytics
from app.utils.paging import Page
from app.utils.templates import templates

router = APIRouter(prefix="/product")


@router.get("")
def view_product_all(store_code: str, req: Request,
                     session: Session = Depends(db.session),
                     sorter: str = Query(default="newest"),
                     q: str = Query(default=None),
                     page: int = Query(default=1, gt=0),
                     page_size: int = Query(default=50),
                     store: Store = Depends(check_store), user: MemberToken = Depends(token_user_option)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    qry = session.query(Product, StoreProduct) \
        .join(StoreProduct, StoreProduct.product_id == Product.id) \
        .join(ProductOption, ProductOption.product_id == Product.id) \
        .filter(StoreProduct.store_code == target_store_code
                , Product.status != 'N'
                , Product.view_yn == 'Y'
                , StoreProduct.view_yn == 'Y'
                , ProductOption.status == 'Y'
                , ProductOption.default_yn == 'Y') \
        .group_by(Product.id)

    if q:
        qry = qry.filter(Product.name.like(f"%{q}%"))

    qry = qry_sorter(qry, sorter)
    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    datas = qry.all()

    paginate = Page(datas, page, page_size, total)

    wish_list, products = wish_and_product_check(session, datas, user, store.code)

    context_data.update(products=products)
    context_data.update(page_title="전체 상품")
    context_data.update(wish_list=wish_list)
    context_data.update(paginate=paginate)
    context_data.update(layout_data=None)

    return templates.TemplateResponse("product-list-grid.html", context=context_data)


@router.get("/search")
def view_product_search(req: Request,
                        q: str = Query(min_length=2),
                        prd: str = Query(default=None),
                        pa: str = Query(default=None),
                        sorter: str = Query(default="newest"),
                        page: int = Query(default=1, gt=0),
                        page_size: int = Query(default=50),
                        session: Session = Depends(db.session),
                        store: Store = Depends(check_store), user: MemberToken = Depends(token_user_option)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    qry = session.query(Product, StoreProduct) \
        .join(StoreProduct, StoreProduct.product_id == Product.id) \
        .join(ProductOption, ProductOption.product_id == Product.id)

    if pa and prd:
        target_pa_list = pa.split(',')
        target_prd_list = prd.split(',')

        qry = qry.filter(StoreProduct.store_code == target_store_code
                         , Product.status != 'N'
                         , Product.view_yn == 'Y'
                         , StoreProduct.view_yn == 'Y'
                         , ProductOption.default_yn == 'Y'
                         , or_(Product.member_id.in_(target_pa_list), Product.id.in_(target_prd_list)))
    elif pa:
        target_pa_list = pa.split(',')

        qry = qry.filter(StoreProduct.store_code == target_store_code
                         , Product.status != 'N'
                         , Product.view_yn == 'Y'
                         , StoreProduct.view_yn == 'Y'
                         , ProductOption.default_yn == 'Y'
                         , Product.member_id.in_(target_pa_list))
    elif prd:
        target_prd_list = prd.split(',')

        qry = qry.filter(StoreProduct.store_code == target_store_code
                         , Product.status != 'N'
                         , Product.view_yn == 'Y'
                         , StoreProduct.view_yn == 'Y'
                         , ProductOption.default_yn == 'Y'
                         , Product.id.in_(target_prd_list))
    else:
        qry = qry.filter(StoreProduct.store_code == target_store_code
                         , Product.status != 'N'
                         , Product.view_yn == 'Y'
                         , StoreProduct.view_yn == 'Y'
                         , ProductOption.default_yn == 'Y'
                         , or_(Product.name.like(f'%{q}%'), Product.keyword.like(f"%{q}%")))

    qry = qry.group_by(Product.id)
    qry = qry_sorter(qry, sorter)
    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    datas = qry.all()

    paginate = Page(datas, page, page_size, total)

    wish_list, products = wish_and_product_check(session, datas, user, store.code)

    context_data.update(products=products)
    context_data.update(page_title=f"검색어: {q}")
    context_data.update(wish_list=wish_list)
    context_data.update(paginate=paginate)
    context_data.update(layout_data=None)

    return templates.TemplateResponse("product-list-grid.html", context=context_data)


@router.get("/{product_id}")
def view_product(store_code: str, product_id: int, req: Request,
                 session: Session = Depends(db.session),
                 store: Store = Depends(check_store),
                 user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    prd = session.query(Product).filter(Product.id == product_id, Product.status != 'N', Product.view_yn == 'Y').first()

    if not prd:
        raise exc.ViewNotFoundEx

    store_prd = session.query(StoreProduct).filter(StoreProduct.product_id == product_id, StoreProduct.store_code == target_store_code, StoreProduct.view_yn == 'Y').first()

    if not store_prd:
        raise exc.NotSaleEx

    product: DataProduct = DataProduct.from_orm(prd)

    cost_variation(product, store_prd)

    check_sold_out(product)

    for row in product.options:
        product.inven_cnt += (row.inventory.count - row.inventory.safe_count)

    categorys = ProductCategory.filter(session, product_id=product_id).all()

    wish = WishProduct.get(session, customer_id=user.id, product_id=product_id, store_code=store.code)

    photo_list = []
    photo_opt_list = []
    for photo in prd.photos:
        if photo.product_option_id:
            photo_opt_list.append(photo)
        else:
            photo_list.append(photo)
    photo_list.extend(photo_opt_list)

    if not photo_list:
        raise exc.NotSaleEx

    context_data.update(product=product)
    context_data.update(is_sold_out=product.is_sold_out)
    context_data.update(photos=photo_list)
    context_data.update(categorys=category(categorys))
    context_data.update(wish=True if wish else False)
    context_data.update(contents=product.contents)

    if product.common_info:
        context_data.update(common_info=product.common_info.contents)

    for row in product.options:
        if row.default_yn == 'Y':
            context_data.update(product_default=row)
            break

    if prd.shipping_info:
        sc: List[ShippingCost] = prd.shipping_info.costs
        shipping_add_cost_text = ""
        for cost in sc:
            if cost.category == "add":
                shipping_add_cost_text = f"제주,도서산간 지역 추가 {'{:,.0f}'.format(cost.cost)}원"

        context_data.update(shipping=dict(
            data=sc,
            type=prd.shipping_info.type,
            pay_type=prd.shipping_info.pay_type,
            calc=prd.shipping_info.calc_type,
            cost=make_shipping_cost_text(sc),
            cost_size=len(sc),
            add_cost=shipping_add_cost_text,
        ))
    else:
        shop = Shop.filter(session, member_id=product.member_id).first()
        context_data.update(shop=shop)

    notice_info = NoticeInfo.filter(session, product_id=product_id).order_by("sort").all()
    if notice_info:
        context_data.update(notice_info=notice_info)

    extra_info = ExtraInfo.filter(session, product_id=product_id).all()
    if extra_info:
        context_data.update(extra_info=extra_info)

    reviews = session.query(ProductReview).filter(ProductReview.product_id == product_id, ProductReview.status == 'Y').all()
    context_data.update(reviews=reviews)

    store_memo = session.query(ProductStoreMemo).filter(ProductStoreMemo.store_code == target_store_code, ProductStoreMemo.product_id == product_id).first()
    if store_memo:
        try:
            context_data.update(store_memo=unquote(b64decode(store_memo.memo).decode('utf-8')))
        except:
            context_data.update(store_memo=None)
    else:
        context_data.update(store_memo=None)

    analytics_data = {
        "store_code": store.code,
        "product_id": product_id,
        "customer_id": user.id if user else None,
        "ip": get_ip(req)
    }
    analytics("view-product", analytics_data)

    return templates.TemplateResponse("shop-product.html", context=context_data)


def category(categorys: List[ProductCategory]):
    target_node = []
    for cate in categorys:
        if cate.category:
            if cate.category.pid in target_node:
                target_node.remove(cate.category.pid)
            target_node.append(cate.category.id)
    result = []
    for cate in categorys:
        if cate.category_id in target_node:
            result.append(cate)
    return result


def get_cost_text(value):
    if value == 0:
        return '무료'
    else:
        return f"{'{:,.0f}'.format(value)}원"


def make_shipping_cost_text(sc: List[ShippingCost]):
    cost_text = ""
    cost_list = []
    for cost in sc:
        if cost.category == "basic":
            if cost.type == "free":
                cost_text = "무료배송"
            elif cost.type == "fix":
                cost_text = get_cost_text(cost.cost)
            elif cost.type in ["cost", "ea", "weight"]:
                cost_list.append(cost)

    if cost_list:
        cost_type = cost_list[0].type
        unit = ""
        info_text = ""
        if cost_type == "cost":
            unit = "원"
            info_text = "금액별"
        elif cost_type == "ea":
            unit = "개"
            info_text = "수량별"
        elif cost_type == "weight":
            unit = "Kg"
            info_text = "중량별"

        if len(cost_list) == 2:
            last_cost = cost_list[1].cost
            section_start = cost_list[1].section_start
            if cost_list[1].section_repeat:
                cost_text = f"{get_cost_text(cost_list[0].cost)} ({'{:,.0f}'.format(section_start)}{unit} 이상 {'{:,.0f}'.format(cost_list[1].section_repeat)}{unit} 마다 {get_cost_text(last_cost)})"
            else:
                cost_text = f"{get_cost_text(cost_list[0].cost)} ({'{:,.0f}'.format(section_start)}{unit} 이상 {get_cost_text(last_cost) if last_cost != 0 else '무료'})"
        else:
            cost_text = f"{get_cost_text(cost_list[0].cost)} ~ {get_cost_text(cost_list.pop().cost)} (구매 {info_text})"

    return cost_text
