from datetime import date

from fastapi import APIRouter, Depends, Query, Security, Body
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Catalog, Store, CatalogStore, Product, CatalogProduct, StoreProduct, ProductCategory, ProductBrand
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.catalog import *
from app.models.common import Success, CreatedID
from app.utils.jwt import token_user
from app.utils.date_utils import D
from app.utils.common_utils import delete_layout_product

router = APIRouter(prefix='/catalog')


@router.post("", response_model=CreatedID, name="카탈로그 등록")
def add_catalog(indata: AddCatalog,
                session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:catalog"])):
    indata_dict = indata.dict()
    data = Catalog.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("", response_model=ListCatalog, name="카탈로그 목록")
def list_catalog(name: Optional[str] = Query(default=None, description="이름"),
                 open: Optional[str] = Query(default=None, description="노출여부"),
                 status: Optional[str] = Query(default=None, description="상태"),
                 s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                 e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                 store_code: Optional[str] = Query(default=None, description="상점 코드"),
                 offset: int = 0, limit: int = 20,
                 session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:catalog"])):
    if store_code:
        qry = session.query(Catalog).join(CatalogStore, Catalog.id == CatalogStore.catalog_id)
        qry = qry.filter(CatalogStore.store_code == store_code, Catalog.open == 'Y')
    else:
        qry = session.query(Catalog)

    if name:
        qry = qry.filter(Catalog.name.like(f'%{name}%'))

    if status:
        qry = qry.filter(Catalog.status == status)

    if open:
        qry = qry.filter(Catalog.open == open)

    if s_reg_date and e_reg_date:
        qry = qry.filter(Catalog.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Catalog.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Catalog.reg_date < D().make235959(e_reg_date))

    qry = qry.order_by(Catalog.reg_date.desc())
    total = qry.count()
    data_list = qry.offset(offset).limit(limit).all()

    return ListCatalog(total=total, datas=data_list)


@router.get("/{catalog_id}", response_model=DataCatalog, name="카탈로그")
def get_catalog(catalog_id: int,
                session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:catalog"])):
    data: Catalog = Catalog.get(session=session, id=catalog_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/{catalog_id}", response_model=Success, name="카탈로그 수정")
def mod_catalog(catalog_id: int, indata: ModCatalog,
                session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:catalog"])):
    data: Catalog = Catalog.get(session=session, id=catalog_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.get("/{catalog_id}/store", response_model=ListCatalogStore, name="카탈로그 상점 목록")
def list_catalog_store_list(catalog_id: int,
                            store_name: Optional[str] = Query(default=None, description="상점 이름"),
                            store_code: Optional[str] = Query(default=None, description="상점 코드"),
                            session: Session = Depends(db.session),
                            offset: int = 0, limit: int = 20,
                            user: MemberToken = Security(token_user, scopes=["read:catalog"])):
    qry = session.query(CatalogStore).join(Store, Store.code == CatalogStore.store_code)
    qry = qry.filter(CatalogStore.catalog_id == catalog_id)

    if store_name:
        qry = qry.filter(Store.title.like(f'%{store_name}%'))

    if store_code:
        qry = qry.filter(CatalogStore.store_code == store_code)

    total = qry.count()
    data_list = qry.offset(offset).limit(limit).all()

    return ListCatalogStore(total=total, datas=data_list)


@router.post("/{catalog_id}/store/link", response_model=Success, name="카탈로그 상점 연결")
def catalog_store_link(catalog_id: int, store_code: str,
                       session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:catalog"])):
    data = Catalog.get(session=session, id=catalog_id)
    if not data:
        raise exc.NotFoundDataEx

    data = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    data = CatalogStore.get(session=session, catalog_id=catalog_id, store_code=store_code)
    if data:
        raise exc.AlreadyDataEx

    CatalogStore.create(session=session, auto_commit=True, store_code=store_code, catalog_id=catalog_id)

    return Success()


@router.delete("/{catalog_id}/store/link", response_model=Success, name="카탈로그 상점 연결 해제")
def catalog_store_unlink(catalog_id: int, store_code: str,
                         session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:catalog"])):
    data: CatalogStore = CatalogStore.get(session=session, catalog_id=catalog_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    sps: List[StoreProduct] = StoreProduct.filter(session, catalog_id=catalog_id, store_code=store_code).all()
    for sp in sps:
        delete_layout_product(session, sp.store_code, sp.product_id)
        StoreProduct.filter(session, id=sp.id).delete(True)

    session.delete(data)
    session.commit()

    return Success()


@router.get("/{catalog_id}/product", response_model=ListCatalogProduct, name="카탈로그 상품 목록")
def list_catalog_product_list(catalog_id: int,
                              name: Optional[str] = Query(default=None, description="상품명"),
                              code: Optional[str] = Query(default=None, description="상품 코드"),
                              member_id: Optional[int] = Query(default=None, description="PA id"),
                              prd_type: Optional[str] = Query(default=None, description="상품유형"),
                              category: Optional[int] = Query(default=None, description="카테고리"),
                              brand: Optional[int] = Query(default=None, description="브랜드"),
                              status: Optional[str] = Query(default=None, description="상품상태"),
                              view_yn: Optional[str] = Query(default=None, description="노출여부"),
                              s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                              e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                              offset: int = 0, limit: int = 20,
                              session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:catalog", "read:catalog_product"])):
    # TODO : read:catalog_product 권한의 경우 자신에게 할당된 카탈로그만 볼수 있음
    if category:
        qry = session.query(CatalogProduct).join(Product, Product.id == CatalogProduct.product_id).outerjoin(ProductCategory, ProductCategory.product_id == Product.id).filter(ProductCategory.category_id == category)
    elif brand:
        qry = session.query(CatalogProduct).join(Product, Product.id == CatalogProduct.product_id).outerjoin(ProductBrand, ProductBrand.product_id == Product.id).filter(ProductBrand.brand_id == brand)
    else:
        qry = session.query(CatalogProduct).join(Product, Product.id == CatalogProduct.product_id)
    qry = qry.filter(CatalogProduct.catalog_id == catalog_id)

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

    return ListCatalogProduct(total=total, datas=data_list)


@router.post("/{catalog_id}/product/link", response_model=Success, name="카탈로그 상품 연결")
def catalog_product_link(catalog_id: int, product_id: List[int],
                         session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:catalog"])):
    data = Catalog.get(session=session, id=catalog_id)
    if not data:
        raise exc.NotFoundDataEx

    for prd_id in product_id:
        data = CatalogProduct.get(session=session, catalog_id=catalog_id, product_id=prd_id)
        if data:
            continue

        CatalogProduct.create(session=session, auto_commit=True, product_id=prd_id, catalog_id=catalog_id)

    return Success()


@router.delete("/{catalog_id}/product/link", response_model=Success, name="카탈로그 상품 연결 해제")
def catalog_product_unlink(catalog_id: int, product_id: List[int],
                           session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:catalog"])):
    for prd_id in product_id:
        data: CatalogProduct = CatalogProduct.get(session=session, catalog_id=catalog_id, product_id=prd_id)
        if not data:
            raise exc.NotFoundDataEx

        sps: List[StoreProduct] = StoreProduct.filter(session, catalog_id=catalog_id, product_id=prd_id).all()
        for sp in sps:
            delete_layout_product(session, sp.store_code, sp.product_id)
            StoreProduct.filter(session, id=sp.id).delete(True)

        session.delete(data)
    session.commit()

    return Success()


@router.put("/{catalog_id}/product/variation", response_model=Success, name="카탈로그 상품 가격 변동값 설정")
def catalog_product_variation(catalog_id: int, variation: int,
                              product_id: Optional[List[int]] = Body(default=None, description="상품 일부만 변경시 사용"),
                              session: Session = Depends(db.session),
                              user: MemberToken = Security(token_user, scopes=["write:catalog"])):
    if product_id:
        for prd_id in product_id:
            data: CatalogProduct = CatalogProduct.get(session=session, catalog_id=catalog_id, product_id=prd_id)
            data.update(session, auto_commit=False, variation=variation)

            StoreProduct.filter(session, catalog_id=catalog_id, product_id=prd_id).update_q(False, variation=variation)
    else:
        CatalogProduct.filter(session, catalog_id=catalog_id).update_q(auto_commit=False, variation=variation)
        StoreProduct.filter(session, catalog_id=catalog_id).update_q(False, variation=variation)

    session.commit()

    return Success()
