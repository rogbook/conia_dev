import json

from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, Shop, Member, Product, StoreProduct
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.utils.common_utils import check_store, make_view_context_data, qry_sorter, get_target_store_code, wish_and_product_check
from app.utils.jwt import token_user_option
from app.utils.templates import templates
from app.utils.paging import Page

router = APIRouter(prefix="/shop")


@router.get("")
def list_shop(store_code: str, req: Request,
              q: str = Query(default=None),
              page: int = Query(default=1, gt=0),
              page_size: int = Query(default=50),
              session: Session = Depends(db.session),
              store: Store = Depends(check_store),
              user: MemberToken = Depends(token_user_option)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    qry = session.query(Shop).join(Member, Member.id == Shop.member_id).join(Product, Product.member_id == Member.id).join(StoreProduct, StoreProduct.product_id == Product.id)
    qry = qry.filter(StoreProduct.store_code == target_store_code, Member.shop_yn == 'Y')

    if q:
        qry = qry.filter(Shop.name.like(f'%{q}%'))

    qry = qry.group_by(Shop.id)
    qry = qry.order_by(Shop.mod_date.desc())

    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    datas = qry.all()

    paginate = Page(datas, page, page_size, total)

    context_data.update(page_title="매장 목록")
    context_data.update(shops=datas)
    context_data.update(paginate=paginate)
    del context_data['layout_data']

    return templates.TemplateResponse("shop-list-grid.html", context=context_data)


@router.get("/{shop_id}")
def view_shop(store_code: str, shop_id: int, req: Request,
              sorter: str = Query(default="newest"),
              q: str = Query(default=None),
              page: int = Query(default=1, gt=0),
              page_size: int = Query(default=50),
              session: Session = Depends(db.session),
              store: Store = Depends(check_store),
              user: MemberToken = Depends(token_user_option)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    qry = session.query(Shop).join(Member, Member.id == Shop.member_id).join(Product, Product.member_id == Member.id).join(StoreProduct, StoreProduct.product_id == Product.id)
    qry = qry.filter(StoreProduct.store_code == target_store_code, Member.shop_yn == 'Y', Shop.id == shop_id)
    shop = qry.first()

    if not shop:
        raise exc.ViewNotFoundEx

    qry = session.query(Product, StoreProduct) \
        .join(StoreProduct, StoreProduct.product_id == Product.id) \
        .filter(StoreProduct.store_code == target_store_code,
                Product.status != 'N',
                Product.view_yn == 'Y',
                StoreProduct.view_yn == 'Y',
                Product.member_id == shop.member_id) \
        .group_by(Product.id)

    if q:
        qry = qry.filter(Product.name.like(f"%{q}%"))

    qry = qry_sorter(qry, sorter)
    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    datas = qry.all()

    paginate = Page(datas, page, page_size, total)

    wish_list, products = wish_and_product_check(session, datas, user, store.code)

    context_data.update(shop=shop)
    context_data.update(products=products)
    context_data.update(page_title=shop.name)
    context_data.update(wish_list=wish_list)
    context_data.update(paginate=paginate)

    return templates.TemplateResponse("shop-product-list-grid.html", context=context_data)
