from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, StoreProduct, Product, LogStore, Shop, Member, ProductCategory, ProductBrand, CatalogProduct, ProductStoreMemo
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, LogStoreDataIn
from app.models.store import *
from app.models.user.shop import ListShop
from app.utils.common_utils import delete_layout_product, log_msg
from app.utils.jwt import token_user

router = APIRouter(prefix='/store')


@router.post("/{store_code}/product/link", response_model=Success, name="상점 상품 연결")
def add_store_product_link(store_code: str, catalog_id: int, target: LinkProduct,
                           session: Session = Depends(db.session),
                           user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    already_cnt = 0
    added_prd_id = []

    for prd in target.products:
        data = StoreProduct.get(session=session, product_id=prd.id, store_code=store_code)
        if data:
            already_cnt += 1
            continue

        StoreProduct.create(session=session, auto_commit=True, product_id=prd.id, store_code=store_code, catalog_id=catalog_id, variation=prd.variation)
        added_prd_id.append(prd.id)

    # 로깅
    log_data = LogStoreDataIn(action="상점 상품 연결", store_code=store_code, msg=log_msg("msg", f'대상 - {added_prd_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.post("/{store_code}/product/link/{catalog_id}", response_model=Success, name="상점 상품 연결(카탈로그 전체)")
def add_store_product_link_catalog(store_code: str, catalog_id: int,
                                   session: Session = Depends(db.session),
                                   user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    catalog_prd_list: List[CatalogProduct] = CatalogProduct.filter(session=session, catalog_id=catalog_id).all()
    if not catalog_prd_list:
        raise exc.NotFoundDataEx

    already_cnt = 0
    added_prd_id = []

    for prd in catalog_prd_list:
        data = StoreProduct.get(session=session, product_id=prd.product_id, store_code=store_code)
        if data:
            already_cnt += 1
            continue

        StoreProduct.create(session=session, auto_commit=False, product_id=prd.product_id, store_code=store_code, catalog_id=catalog_id, variation=prd.variation)
        added_prd_id.append(prd.id)
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상점 상품 연결", store_code=store_code, msg=log_msg("msg", f'카탈로그({catalog_id}) 전체 연결 / 대상 - {added_prd_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/{store_code}/product/link", response_model=Success, name="상점 상품 연결 해제")
def del_store_product_link(store_code: str, product_id: List[int],
                           session: Session = Depends(db.session),
                           user: MemberToken = Security(token_user, scopes=['write:store'])):
    for prd_id in product_id:
        data: StoreProduct = StoreProduct.get(session=session, product_id=prd_id, store_code=store_code)
        if not data:
            raise exc.NotFoundDataEx

        session.delete(data)
        delete_layout_product(session, store_code, prd_id)

    # 로깅
    log_data = LogStoreDataIn(action="상점 상품 연결 해제", store_code=store_code, msg=log_msg("msg", f'대상 - {product_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    session.commit()

    return Success()


@router.put("/{store_code}/product/{product_id}/link", response_model=Success, name="상점 상품 연결 수정")
def mod_store_product_link(store_code: str, product_id: int, view_yn: str,
                           session: Session = Depends(db.session),
                           user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: StoreProduct = StoreProduct.get(session=session, product_id=product_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    change_data = data.update_optional(session=session, auto_commit=True, view_yn=view_yn)

    # 로깅
    log_data = LogStoreDataIn(action="상점 상품 연결 수정", store_code=store_code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/product", response_model=ListCatalogProduct, name="상점 상품 목록")
def list_store_product(store_code: str,
                       name: Optional[str] = Query(default=None, description="상품명"),
                       code: Optional[str] = Query(default=None, description="상품 코드"),
                       category: Optional[int] = Query(default=None, description="카테고리"),
                       brand: Optional[int] = Query(default=None, description="브랜드"),
                       prd_type: Optional[str] = Query(default=None, description="상품유형"),
                       member_id: Optional[int] = Query(default=None, description="PA id"),
                       status: Optional[str] = Query(default=None, description="상품상태"),
                       view_yn: Optional[str] = Query(default=None, description="노출여부"),
                       catalog_id: Optional[int] = Query(default=None, description="카탈로그 ID"),
                       offset: int = 0, limit: int = 20,
                       session: Session = Depends(db.session),
                       user: MemberToken = Security(token_user, scopes=['read:store'])):
    if category:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id).outerjoin(ProductCategory, ProductCategory.product_id == Product.id).filter(ProductCategory.category_id == category)
    elif brand:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id).outerjoin(ProductBrand, ProductBrand.product_id == Product.id).filter(ProductBrand.brand_id == brand)
    else:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id)

    qry = qry.filter(StoreProduct.store_code == store_code)

    if name:
        qry = qry.filter(Product.name.like(f'%{name}%'))

    if code:
        qry = qry.filter(Product.code.like(f'%{code}%'))

    if prd_type:
        qry = qry.filter(Product.type.like(f'{prd_type}%'))

    if member_id:
        qry = qry.filter(Product.member_id == member_id)

    if status:
        qry = qry.filter(Product.status == status)

    if view_yn:
        qry = qry.filter(Product.view_yn == view_yn)

    if catalog_id:
        qry = qry.filter(StoreProduct.catalog_id == catalog_id)

    total = qry.count()
    qry = qry.order_by(Product.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListCatalogProduct(total=total, datas=data_list)


@router.get("/{store_code}/shop", response_model=ListShop, name="상점 매장 목록")
def list_store_shop(store_code: str,
                    name: Optional[str] = Query(default=None, description="매장명"),
                    offset: int = 0, limit: int = 20,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['read:store'])):
    qry = session.query(Shop).join(Member, Member.id == Shop.member_id).join(Product, Product.member_id == Member.id).join(StoreProduct, StoreProduct.product_id == Product.id)
    qry = qry.filter(StoreProduct.store_code == store_code, Member.shop_yn == 'Y')

    if name:
        qry = qry.filter(Shop.name.like(f'%{name}%'))

    qry = qry.group_by(Shop.id)

    total = qry.count()
    qry = qry.order_by(Product.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListShop(total=total, datas=data_list)


@router.post("/{store_code}/product/memo/list", response_model=Success, name="상점 상품 추가설명 등록 [목록]")
def add_store_product_memo_list(store_code: str, indata: MemoProduct,
                                session: Session = Depends(db.session),
                                user: MemberToken = Security(token_user, scopes=['write:store'])):
    store: Store = Store.get(session=session, code=store_code)
    if not store:
        raise exc.NotFoundDataEx

    for prd_id in indata.products:
        prd_memo = ProductStoreMemo.get(session=session, product_id=prd_id, store_code=store_code)
        if prd_memo:
            prd_memo.memo = indata.memo
            continue

        ProductStoreMemo.create(session=session, auto_commit=False, product_id=prd_id, store_code=store_code, member_id=user.id, memo=indata.memo)
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상품 추가설명 등록", store_code=store_code, msg=log_msg("msg", f'대상 - {indata.products}\n내용 - {indata.memo}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.post("/{store_code}/product/memo/search", response_model=Success, name="상점 상품 추가설명 등록 [검색]")
def add_store_product_memo_search(store_code: str,
                                  indata: MemoOnlyProduct,
                                  name: Optional[str] = Query(default=None, description="상품명"),
                                  code: Optional[str] = Query(default=None, description="상품 코드"),
                                  category: Optional[int] = Query(default=None, description="카테고리"),
                                  brand: Optional[int] = Query(default=None, description="브랜드"),
                                  prd_type: Optional[str] = Query(default=None, description="상품유형"),
                                  member_id: Optional[int] = Query(default=None, description="PA id"),
                                  status: Optional[str] = Query(default=None, description="상품상태"),
                                  view_yn: Optional[str] = Query(default=None, description="노출여부"),
                                  catalog_id: Optional[int] = Query(default=None, description="카탈로그 ID"),
                                  session: Session = Depends(db.session),
                                  user: MemberToken = Security(token_user, scopes=['read:store'])):
    if category:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id).outerjoin(ProductCategory, ProductCategory.product_id == Product.id).filter(ProductCategory.category_id == category)
    elif brand:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id).outerjoin(ProductBrand, ProductBrand.product_id == Product.id).filter(ProductBrand.brand_id == brand)
    else:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id)

    qry = qry.filter(StoreProduct.store_code == store_code)

    if name:
        qry = qry.filter(Product.name.like(f'%{name}%'))

    if code:
        qry = qry.filter(Product.code.like(f'%{code}%'))

    if prd_type:
        qry = qry.filter(Product.type.like(f'{prd_type}%'))

    if member_id:
        qry = qry.filter(Product.member_id == member_id)

    if status:
        qry = qry.filter(Product.status == status)

    if view_yn:
        qry = qry.filter(Product.view_yn == view_yn)

    if catalog_id:
        qry = qry.filter(StoreProduct.catalog_id == catalog_id)

    data_list = qry.all()

    prd_ids = []

    for store_prd in data_list:
        prd_ids.append(store_prd.product_id)
        prd_memo = ProductStoreMemo.get(session=session, product_id=store_prd.product_id, store_code=store_code)
        if prd_memo:
            prd_memo.memo = indata.memo
            continue

        ProductStoreMemo.create(session=session, auto_commit=False, product_id=store_prd.product_id, store_code=store_code, member_id=user.id, memo=indata.memo)
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상품 추가설명 등록", store_code=store_code, msg=log_msg("msg", f'대상 - {prd_ids}\n내용 - {indata.memo}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/product/memo/{product_id}", name="상점 상품 추가설명")
def get_store_product_memo(store_code: str,
                           product_id: int,
                           session: Session = Depends(db.session),
                           user: MemberToken = Security(token_user, scopes=['read:store'])):
    data = ProductStoreMemo.get(session=session, store_code=store_code, product_id=product_id)
    if data is None:
        raise exc.NotFoundDataEx

    return data


@router.delete("/{store_code}/product/memo/list", response_model=Success, name="상점 상품 추가설명 삭제 [목록]")
def del_store_product_memo_list(store_code: str,
                                target: List[int],
                                session: Session = Depends(db.session),
                                user: MemberToken = Security(token_user, scopes=['write:store'])):
    store: Store = Store.get(session=session, code=store_code)
    if not store:
        raise exc.NotFoundDataEx

    for prd_id in target:
        prd_memo = ProductStoreMemo.get(session=session, product_id=prd_id, store_code=store_code)
        if prd_memo:
            session.delete(prd_memo)
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상품 추가설명 삭제", store_code=store_code, msg=log_msg("msg", f'대상 - {target}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/{store_code}/product/memo/search", response_model=Success, name="상점 상품 추가설명 삭제 [검색]")
def del_store_product_memo_search(store_code: str,
                                  name: Optional[str] = Query(default=None, description="상품명"),
                                  code: Optional[str] = Query(default=None, description="상품 코드"),
                                  category: Optional[int] = Query(default=None, description="카테고리"),
                                  brand: Optional[int] = Query(default=None, description="브랜드"),
                                  prd_type: Optional[str] = Query(default=None, description="상품유형"),
                                  member_id: Optional[int] = Query(default=None, description="PA id"),
                                  status: Optional[str] = Query(default=None, description="상품상태"),
                                  view_yn: Optional[str] = Query(default=None, description="노출여부"),
                                  session: Session = Depends(db.session),
                                  user: MemberToken = Security(token_user, scopes=['read:store'])):
    if category:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id).outerjoin(ProductCategory, ProductCategory.product_id == Product.id).filter(ProductCategory.category_id == category)
    elif brand:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id).outerjoin(ProductBrand, ProductBrand.product_id == Product.id).filter(ProductBrand.brand_id == brand)
    else:
        qry = session.query(StoreProduct).join(Product, Product.id == StoreProduct.product_id)

    qry = qry.filter(StoreProduct.store_code == store_code)

    if name:
        qry = qry.filter(Product.name.like(f'%{name}%'))

    if code:
        qry = qry.filter(Product.code.like(f'%{code}%'))

    if prd_type:
        qry = qry.filter(Product.type.like(f'{prd_type}%'))

    if member_id:
        qry = qry.filter(Product.member_id == member_id)

    if status:
        qry = qry.filter(Product.status == status)

    if view_yn:
        qry = qry.filter(Product.view_yn == view_yn)

    data_list = qry.all()

    prd_ids = []

    for store_prd in data_list:
        prd_ids.append(store_prd.product_id)
        prd_memo = ProductStoreMemo.get(session=session, product_id=store_prd.product_id, store_code=store_code)
        if prd_memo:
            session.delete(prd_memo)
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상품 추가설명 삭제", store_code=store_code, msg=log_msg("msg", f'대상 - {prd_ids}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()
