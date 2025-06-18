from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, Product, StoreProduct, ProductCategory, Category, ProductOption
from app.models.auth import MemberToken
from app.utils.common_utils import check_store, make_view_context_data, sub_category, qry_sorter, get_target_store_code, wish_and_product_check
from app.utils.jwt import token_user_option
from app.utils.paging import Page
from app.utils.templates import templates

router = APIRouter(prefix="/category")


@router.get("/{category_id}")
def view_category(category_id: int, request: Request,
                  q: str = Query(default=None),
                  sorter: str = Query(default="newest"),
                  page: int = Query(default=1, gt=0),
                  page_size: int = Query(default=50),
                  session: Session = Depends(db.session),
                  store: Store = Depends(check_store), user: MemberToken = Depends(token_user_option)):
    context_data = make_view_context_data(session, request, store, user)

    target_store_code = get_target_store_code(context_data)

    qry = session.query(Product, StoreProduct) \
        .join(StoreProduct, StoreProduct.product_id == Product.id) \
        .join(ProductCategory, ProductCategory.product_id == Product.id) \
        .join(ProductOption, ProductOption.product_id == Product.id) \
        .filter(StoreProduct.store_code == target_store_code,
                Product.status != 'N',
                Product.view_yn == 'Y',
                StoreProduct.view_yn == 'Y',
                ProductOption.default_yn == 'Y',
                ProductCategory.category_id == category_id) \
        .group_by(Product.id)

    if q:
        qry = qry.filter(Product.name.like(f"%{q}%"))

    qry = qry_sorter(qry, sorter)
    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    datas = qry.all()

    paginate = Page(datas, page, page_size, total)

    wish_list, products = wish_and_product_check(session, datas, user, store.code)

    category = Category.get(session=session, id=category_id)

    context_data.update(products=products)
    context_data.update(page_title=category.name)
    context_data.update(current_category=category)
    context_data.update(wish_list=wish_list)
    context_data.update(paginate=paginate)
    context_data.update(layout_data=None)

    category_data = context_data.get("category")
    sub = sub_category(category_data, category_id)
    context_data.update(sub_category=sub)
    return templates.TemplateResponse("product-list-grid.html", context=context_data)
