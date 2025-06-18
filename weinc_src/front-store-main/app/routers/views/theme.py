import json

from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, StoreTheme, Category, StoreThemeProduct, ProductCategory, Product, StoreProduct, Shop, StoreThemeShop, ProductOption
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.utils.common_utils import check_store, make_view_context_data, update_shop, qry_sorter, get_target_store_code, wish_and_product_check
from app.utils.jwt import token_user_option
from app.utils.templates import templates
from app.utils.paging import Page

router = APIRouter(prefix="/theme")


@router.get("/{theme_id}")
def view_theme(store_code: str, theme_id: int, req: Request,
               sorter: str = Query(default="newest"),
               q: str = Query(default=None),
               page: int = Query(default=1, gt=0),
               page_size: int = Query(default=50),
               session: Session = Depends(db.session),
               store: Store = Depends(check_store),
               user: MemberToken = Depends(token_user_option)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    theme: StoreTheme = session.query(StoreTheme).filter(
        StoreTheme.id == theme_id,
        StoreTheme.store_code == target_store_code,
        StoreTheme.status == 'Y').first()

    if not theme:
        raise exc.ViewNotFoundEx

    context_data.update(theme=theme)
    context_data.update(page_title=theme.name)

    bottom_themes = session.query(StoreTheme).filter(StoreTheme.pid == theme_id, StoreTheme.status == 'Y', StoreTheme.visible == 'Y').order_by(StoreTheme.sort).all()
    context_data.update(bottom_themes=bottom_themes)
    context_data.update(sibling_themes=None)

    if theme.pid:
        sibling_themes = session.query(StoreTheme).filter(StoreTheme.pid == theme.pid, StoreTheme.status == 'Y', StoreTheme.visible == 'Y').order_by(StoreTheme.sort).all()
        context_data.update(sibling_themes=sibling_themes)

        top_theme = session.query(StoreTheme).filter(StoreTheme.id == theme.pid).first()
        context_data.update(top_theme=top_theme)

    if theme.use_layout == 'Y' or theme.use_layout == 'L':  # 레이아웃 타입
        context_data.update(layout_data=json.loads(theme.layout) if theme.layout else None)
        update_shop(session, context_data)
        return templates.TemplateResponse("index.jinja2", context=context_data)
    elif theme.use_layout == 'S':  # 매장 타입
        qry = session.query(Shop).join(StoreThemeShop, Shop.id == StoreThemeShop.shop_id)
        qry = qry.filter(StoreThemeShop.store_theme_id == theme_id)

        if q:
            qry = qry.filter(Shop.name.like(f'%{q}%'))

        if sorter == 'name':
            qry = qry.order_by(Shop.name.asc())
        else:
            qry = qry.order_by(Shop.mod_date.desc())

        total = qry.count()
        qry = qry.offset(page_size * (page - 1)).limit(page_size)
        datas = qry.all()

        paginate = Page(datas, page, page_size, total)

        context_data.update(shops=datas)
        context_data.update(paginate=paginate)

        context_data.update(layout_data=json.loads(theme.layout) if theme.layout else None)
        # update_product(session, context_data, user, store_code)

        return templates.TemplateResponse("shop-list-grid.html", context=context_data)
    else:  # 상품 타입
        qry = session.query(Product, StoreProduct) \
            .join(StoreProduct, StoreProduct.product_id == Product.id) \
            .join(StoreThemeProduct, StoreThemeProduct.product_id == Product.id) \
            .join(ProductOption, ProductOption.product_id == Product.id) \
            .filter(StoreThemeProduct.store_theme_id == theme_id,
                    StoreProduct.store_code == target_store_code,
                    Product.view_yn == 'Y',
                    StoreProduct.view_yn == 'Y',
                    ProductOption.status == 'Y',
                    ProductOption.default_yn == 'Y') \
            .group_by(Product.id)

        if q:
            qry = qry.filter(Product.name.like(f"%{q}%"))

        qry = qry_sorter(qry, sorter)
        total = qry.count()
        qry = qry.offset(page_size * (page - 1)).limit(page_size)
        datas = qry.all()

        paginate = Page(datas, page, page_size, total)

        wish_list, products = wish_and_product_check(session, datas, user, store.code)

        context_data.update(wish_list=wish_list)
        context_data.update(products=products)
        context_data.update(paginate=paginate)

        context_data.update(layout_data=json.loads(theme.layout) if theme.layout else None)
        # update_product(session, context_data, user, store_code)

        return templates.TemplateResponse("product-list-grid.html", context=context_data)
