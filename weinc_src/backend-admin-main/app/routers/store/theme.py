from datetime import date

from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import StoreTheme, Product, StoreThemeProduct, LogStore, Shop, StoreThemeShop, ProductCategory, ProductBrand
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, EnumSearchType, LogStoreDataIn
from app.models.product.product import ListDataProduct
from app.models.store import *
from app.utils.common_utils import list_to_dict, make_tree, log_msg
from app.utils.date_utils import D
from app.utils.jwt import token_user
from app.models.user.shop import ListShop

router = APIRouter(prefix='/store')


@router.post("/{store_code}/theme", response_model=Success, name="상점 테마 등록")
def add_store_theme(store_code: str, indata: AddStoreTheme,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store'])):
    indata_dict = indata.dict()
    StoreTheme.create(session, auto_commit=True, **indata_dict)

    # 로깅
    log_data = LogStoreDataIn(action="테마 등록", store_code=indata.store_code, msg=log_msg("msg", f'테마 등록 - {indata.name}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/theme/list/{search_type}", response_model=Union[List[SubStoreTheme], List[DataStoreTheme]], name="상점 테마 전체 목록")
def all_store_theme(store_code: str, search_type: EnumSearchType,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['read:store'])):
    if search_type is EnumSearchType.top:
        data_list = session.query(StoreTheme).filter(StoreTheme.store_code == store_code, StoreTheme.pid == None, StoreTheme.status != 'D').all()
        return data_list

    if search_type is EnumSearchType.all:
        data_list_top = session.query(StoreTheme).filter(StoreTheme.store_code == store_code, StoreTheme.status != 'D').all()
        data = list_to_dict(data_list_top)
        return make_tree(data)


@router.get("/{store_code}/theme/{theme_id}", response_model=List[DataStoreTheme], name="상점 테마 하위 목록")
def sub_store_theme(store_code: str, theme_id: int,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['read:store'])):
    data_list = session.query(StoreTheme).filter(StoreTheme.store_code == store_code, StoreTheme.pid == theme_id, StoreTheme.status != 'D').all()

    return data_list


@router.put("/{store_code}/theme/{theme_id}", response_model=Success, name="상점 테마 수정")
def mod_store_theme(store_code: str, theme_id: int, indata: ModStoreTheme,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: StoreTheme = StoreTheme.get(session=session, id=theme_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action="테마 수정", store_code=store_code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/theme/{theme_id}/product", response_model=ListDataProduct, name="상점 테마 상품 목록")
def store_theme_product(store_code: str, theme_id: int,
                        name: Optional[str] = Query(default=None, description="상품명"),
                        code: Optional[str] = Query(default=None, description="상품 코드"),
                        member_id: Optional[int] = Query(default=None, description="PA id"),
                        category: Optional[int] = Query(default=None, description="카테고리"),
                        brand: Optional[int] = Query(default=None, description="브랜드"),
                        prd_type: Optional[str] = Query(default=None, description="상품유형"),
                        status: Optional[str] = Query(default=None, description="상품상태"),
                        view_yn: Optional[str] = Query(default=None, description="노출여부"),
                        s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                        e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                        offset: int = 0, limit: int = 20,
                        session: Session = Depends(db.session),
                        user: MemberToken = Security(token_user, scopes=['read:store'])):
    check_theme(session, theme_id, store_code)

    if category:
        qry = session.query(Product).join(StoreThemeProduct, Product.id == StoreThemeProduct.product_id).outerjoin(ProductCategory, ProductCategory.product_id == Product.id).filter(ProductCategory.category_id == category)
    elif brand:
        qry = session.query(Product).join(StoreThemeProduct, Product.id == StoreThemeProduct.product_id).outerjoin(ProductBrand, ProductBrand.product_id == Product.id).filter(ProductBrand.brand_id == brand)
    else:
        qry = session.query(Product).join(StoreThemeProduct, Product.id == StoreThemeProduct.product_id)

    qry = qry.filter(StoreThemeProduct.store_theme_id == theme_id)

    if name:
        qry = qry.filter(Product.name.like(f'%{name}%'))

    if code:
        qry = qry.filter(Product.code.like(f'%{code}%'))

    if member_id:
        qry = qry.filter(Product.member_id == member_id)

    if prd_type:
        qry = qry.filter(Product.type.like(f'{prd_type}%'))

    if status:
        qry = qry.filter(Product.status == status)

    if view_yn:
        qry = qry.filter(Product.view_yn == view_yn)

    if s_reg_date and e_reg_date:
        qry = qry.filter(Product.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Product.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Product.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(Product.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListDataProduct(total=total, datas=data_list)


@router.post("/{store_code}/theme/{theme_id}/link", response_model=Success, name="상점 테마 상품 연결")
def link_store_theme(store_code: str, theme_id: int, product_id: List[int],
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:store'])):
    theme = check_theme(session, theme_id, store_code)

    added_prd_id = []

    for prd_id in product_id:
        prd = Product.get(session=session, id=prd_id)
        if not prd:
            raise exc.NotFoundDataEx
        data = StoreThemeProduct.get(session=session, store_theme_id=theme_id, product_id=prd_id)
        if data:
            continue

        mapping_data = {
            "product_id": prd_id,
            "store_theme_id": theme_id,
        }
        StoreThemeProduct.create(session=session, auto_commit=True, **mapping_data)
        added_prd_id.append(prd.id)

    # 로깅
    log_data = LogStoreDataIn(action="상점 테마 상품 연결", store_code=store_code, msg=log_msg("msg", f'테마 - {theme.name}:{theme.id} / 대상 - {added_prd_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/{store_code}/theme/{theme_id}/link", response_model=Success, name="상점 테마 상품 연결 해제")
def unlink_store_theme(store_code: str, theme_id: int, product_id: List[int],
                       session: Session = Depends(db.session),
                       user: MemberToken = Security(token_user, scopes=['write:store'])):
    theme = check_theme(session, theme_id, store_code)

    for prd_id in product_id:
        prd = Product.get(session=session, id=prd_id)
        if not prd:
            raise exc.NotFoundDataEx
        data = StoreThemeProduct.get(session=session, store_theme_id=theme_id, product_id=prd_id)
        if not data:
            raise exc.NotFoundDataEx

        session.delete(data)
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상점 테마 상품 연결 해제", store_code=store_code, msg=log_msg("msg", f'테마 - {theme.name}:{theme.id} / 대상 - {product_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/theme/{theme_id}/shop", response_model=ListShop, name="상점 테마 매장 목록")
def theme_shop(store_code: str, theme_id: int,
               name: Optional[str] = Query(default=None, description="매장명"),
               member_id: Optional[int] = Query(default=None, description="PA id"),
               offset: int = 0, limit: int = 20,
               session: Session = Depends(db.session),
               user: MemberToken = Security(token_user, scopes=['read:store'])):
    check_theme(session, theme_id, store_code)

    qry = session.query(Shop).join(StoreThemeShop, Shop.id == StoreThemeShop.shop_id)
    qry = qry.filter(StoreThemeShop.store_theme_id == theme_id)

    if name:
        qry = qry.filter(Shop.name.like(f'%{name}%'))

    if member_id:
        qry = qry.filter(Shop.member_id == member_id)

    total = qry.count()
    data_list = qry.offset(offset).limit(limit).all()

    return ListShop(total=total, datas=data_list)


@router.post("/{store_code}/theme/{theme_id}/shop_link", response_model=Success, name="상점 테마 매장 연결")
def link_theme_shop(store_code: str, theme_id: int, shop_id: List[int],
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store'])):
    theme = check_theme(session, theme_id, store_code)

    added_id = []

    for s_id in shop_id:
        shop = Shop.get(session=session, id=s_id)
        if not shop:
            raise exc.NotFoundDataEx
        data = StoreThemeShop.get(session=session, store_theme_id=theme_id, shop_id=s_id)
        if data:
            continue

        mapping_data = {
            "shop_id": s_id,
            "store_theme_id": theme_id,
        }
        StoreThemeShop.create(session=session, auto_commit=True, **mapping_data)
        added_id.append(shop.id)

    # 로깅
    log_data = LogStoreDataIn(action="상점 테마 매장 연결", store_code=store_code, msg=log_msg("msg", f'테마 - {theme.name}:{theme.id} / 대상 - {added_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/{store_code}/theme/{theme_id}/shop_link", response_model=Success, name="상점 테마 매장 연결 해제")
def unlink_theme_shop(store_code: str, theme_id: int, shop_id: List[int],
                      session: Session = Depends(db.session),
                      user: MemberToken = Security(token_user, scopes=['write:store'])):
    theme = check_theme(session, theme_id, store_code)

    for s_id in shop_id:
        shop = Shop.get(session=session, id=s_id)
        if not shop:
            raise exc.NotFoundDataEx
        data = StoreThemeShop.get(session=session, store_theme_id=theme_id, shop_id=s_id)
        if not data:
            raise exc.NotFoundDataEx

        session.delete(data)
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상점 테마 매장 연결 해제", store_code=store_code, msg=log_msg("msg", f'테마 - {theme.name}:{theme.id} / 대상 - {shop_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


def check_theme(session, theme_id, store_code):
    data = StoreTheme.get(session=session, id=theme_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx
    return data
