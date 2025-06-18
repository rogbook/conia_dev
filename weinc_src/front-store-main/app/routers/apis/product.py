from fastapi import APIRouter, Depends, UploadFile, Request, Form, Response
from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import uuid4

from fastapi_cache.decorator import cache

from app.utils.jwt import token_user
from app.utils.common_utils import extensions_check, get_extensions, get_ip, check_sold_out
from app.utils.aws import S3
from app.utils.date_utils import D
from app.utils.log import data_logger
from app.errors import exceptions as exc
from app.common.consts import AWS_S3_BUCKET_IMG, AWS_IMG_HOST

from app.database.conn import db
from app.database.schema import Product, ProductReview, ProductReviewPhoto, ProductOption, StoreProduct, ProductQna, OrderProduct, Store

from app.models.common import Success, CreatedID
from app.models.product import DataProduct, AddProductReview, DataProductReview, ModProductReview, DataOptions, AddProductQna
from app.models.auth import MemberToken

router = APIRouter(prefix='/product')


def request_key_builder(
        func,
        namespace: str = "",
        request: Request = None,
        response: Response = None,
        *args,
        **kwargs):
    return ":".join([
        namespace,
        request.method.lower(),
        request.url.path,
        repr(sorted(request.query_params.items()))
    ])


@router.get("", name="상품 정보", response_model=DataProduct)
@cache(expire=60 * 5, key_builder=request_key_builder)
def get_product(store_code: str,
                product_id: int,
                session: Session = Depends(db.session)):
    prd = session.query(Product).filter(Product.id == product_id, Product.status != 'D').first()
    if not prd:
        raise exc.NotFoundDataEx

    store = Store.get(session, code=store_code)
    if not store:
        raise exc.NotFoundDataEx

    dupl_target = None
    if store.dupl_store:
        dupl_target = Store.get(session, code=store.dupl_store)

    if dupl_target:
        store = dupl_target

    sp = StoreProduct.get(session, store_code=store.code, product_id=product_id)
    if not sp:
        raise exc.NotFoundDataEx

    data = DataProduct.from_orm(prd)
    variation = sp.variation
    for opt in data.options:
        if opt.default_yn == 'Y':
            option = DataOptions.from_orm(opt)
            if variation != 0:
                option.selling_price = option.selling_price + variation
            data.product_default = option

        data.inven_cnt += (opt.inventory.count - opt.inventory.safe_count)
    check_sold_out(data)

    return data


@router.get("/option", name="상품옵션 정보")
def get_option(store_code: str,
               product_id: int,
               selected: str = None,
               session: Session = Depends(db.session),
               user: MemberToken = Depends(token_user)):
    prd = session.query(Product).filter(Product.id == product_id, Product.status != 'D').first()
    if not prd:
        raise exc.NotFoundDataEx

    store = Store.get(session, code=store_code)
    original_store = store
    dupl_target = None
    if store.dupl_store:
        dupl_target = Store.get(session, code=store.dupl_store)

    if dupl_target:
        store = dupl_target

    sp = StoreProduct.get(session, store_code=store.code, product_id=product_id)
    if not sp:
        raise exc.NotFoundDataEx

    option_list: List[ProductOption] = ProductOption.filter(session, product_id=product_id, status='Y').all()
    if not option_list:
        raise exc.NotFoundDataEx

    default_price = 0

    options: List[DataOptions] = []
    for row in option_list:
        data = DataOptions.from_orm(row)
        if sp.variation != 0:
            data.selling_price = data.selling_price + sp.variation
        is_sold_out = False
        if prd.status == 'S':
            data.is_sold_out = True
        elif prd.inven_use == "Y":
            if row.inventory.count <= row.inventory.safe_count:
                is_sold_out = True
            data.is_sold_out = is_sold_out
        options.append(data)

    for row in options:
        if row.default_yn == "Y":
            default_price = row.selling_price

    option_kind = option_list[0].option_title.split(",")
    kind_cnt = len(option_kind)

    result = []

    if selected:
        selected_options = selected.split(",")
        selected_cnt = len(selected_options)

        for row in options:
            if row.view_yn != "Y":
                continue
            if selected_cnt == 1:
                if row.option_1 == selected_options[0]:
                    if {"title": row.option_2} not in result and row.option_2:
                        data = dict(title=row.option_2)
                        if selected_cnt == kind_cnt - 1:
                            data.update(option_id=row.id)
                            data.update(add_text=add_text(default_price, row.selling_price, row.inventory.count if prd.inven_use == "Y" and prd.view_inventory == 'Y' else None))
                            data.update(is_sold_out=row.is_sold_out)
                        result.append(data)
            elif selected_cnt == 2:
                if row.option_1 == selected_options[0] and row.option_2 == selected_options[1]:
                    if {"title": row.option_3} not in result and row.option_3:
                        data = dict(title=row.option_3)
                        if selected_cnt == kind_cnt - 1:
                            data.update(option_id=row.id)
                            data.update(add_text=add_text(default_price, row.selling_price, row.inventory.count if prd.inven_use == "Y" and prd.view_inventory == 'Y' else None))
                            data.update(is_sold_out=row.is_sold_out)
                        result.append(data)
            elif selected_cnt == 3:
                if row.option_1 == selected_options[0] and row.option_2 == selected_options[1] and row.option_3 == selected_options[2]:
                    if {"title": row.option_4} not in result and row.option_4:
                        data = dict(title=row.option_4)
                        if selected_cnt == kind_cnt - 1:
                            data.update(option_id=row.id)
                            data.update(add_text=add_text(default_price, row.selling_price, row.inventory.count if prd.inven_use == "Y" and prd.view_inventory == 'Y' else None))
                            data.update(is_sold_out=row.is_sold_out)
                        result.append(data)
            elif selected_cnt == 4:
                if row.option_1 == selected_options[0] and row.option_2 == selected_options[1] and row.option_3 == selected_options[2] and row.option_4 == selected_options[3]:
                    if {"title": row.option_5} not in result and row.option_5:
                        data = dict(title=row.option_5)
                        if selected_cnt == kind_cnt - 1:
                            data.update(option_id=row.id)
                            data.update(add_text=add_text(default_price, row.selling_price, row.inventory.count if prd.inven_use == "Y" and prd.view_inventory == 'Y' else None))
                            data.update(is_sold_out=row.is_sold_out)
                        result.append(data)
    else:
        for row in options:
            if row.view_yn != "Y":
                continue
            if {"title": row.option_1} not in result:
                data = dict(title=row.option_1)
                if 0 == kind_cnt - 1:
                    data.update(option_id=row.id)
                    data.update(add_text=add_text(default_price, row.selling_price, row.inventory.count if prd.inven_use == "Y" and prd.view_inventory == 'Y' else None))
                    data.update(is_sold_out=row.is_sold_out)
                result.append(data)

    return result


@router.post("/review", response_model=Success, name="상품 리뷰 등록")
def add_product_review(req: Request,
                       files: Optional[List[UploadFile]] = Form(default=None),
                       order_product_id: int = Form(),
                       contents: str = Form(),
                       order_info: Optional[str] = Form(default=None),
                       session: Session = Depends(db.session),
                       member: MemberToken = Depends(token_user)):
    op: OrderProduct = OrderProduct.get(session, id=order_product_id)
    if not op:
        raise exc.NotFoundDataEx

    pr = ProductReview()
    pr.product_id = op.product_id
    pr.contents = contents
    pr.order_info = order_info
    pr.order_product_id = order_product_id
    pr.customer_id = member.id

    session.add(pr)
    session.flush()
    session.commit()

    if files:
        for file in files:
            if not extensions_check(file.filename):
                raise exc.NotAllowedFileEx

        s3 = S3()
        for file in files:
            file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{get_extensions(file.filename)}"
            s3.upload_file(file, AWS_S3_BUCKET_IMG, 'review/', file_name)
            url: str = f"{AWS_IMG_HOST}review/{file_name}"

            log_dict = dict(
                category="product",
                action="add",
                type="review_photo",
                ip=get_ip(req),
                user=member.id,
                user_name=member.name,
                data=url,
            )
            data_logger(log_dict)

            ProductReviewPhoto.create(session, auto_commit=True, product_review_id=pr.id, uri=url)

    return Success()


@router.put("/review/{review_id}", response_model=Success, name="상품 리뷰 수정")
def mod_product_review(review_id: int,
                       indata: ModProductReview,
                       session: Session = Depends(db.session),
                       user: MemberToken = Depends(token_user)):
    data: ProductReview = ProductReview.get(session=session, id=review_id, customer_id=user.id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/review/{review_id}/photo", response_model=Success, name="상품 리뷰 사진 등록")
def add_product_review_photo(review_id: int,
                             files: List[UploadFile],
                             req: Request,
                             session: Session = Depends(db.session),
                             user: MemberToken = Depends(token_user)):
    data: ProductReview = ProductReview.get(session=session, id=review_id, customer_id=user.id)
    if not data:
        raise exc.NotFoundDataEx

    for file in files:
        if not extensions_check(file.filename):
            raise exc.NotAllowedFileEx

    s3 = S3()
    for file in files:
        file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{get_extensions(file.filename)}"
        s3.upload_file(file, AWS_S3_BUCKET_IMG, 'review/', file_name)
        url: str = f"{AWS_IMG_HOST}review/{file_name}"

        log_dict = dict(
            category="product",
            action="add",
            type="review",
            ip=get_ip(req),
            user=user.id,
            user_name=user.name,
            data=url,
        )
        data_logger(log_dict)

        ProductReviewPhoto.create(session, auto_commit=True, product_review_id=review_id, uri=url)

    return Success()


@router.delete("/review/{review_id}", response_model=Success, name="상품 리뷰 삭제")
def del_product_review(review_id: int,
                       session: Session = Depends(db.session),
                       member: MemberToken = Depends(token_user)):
    data = ProductReview.get(session, id=review_id, customer_id=member.id)
    if not data:
        raise exc.NotFoundDataEx

    data.status = 'D'
    session.commit()

    return Success()


@router.delete("/review/{review_id}/photo", response_model=Success, name="상품 리뷰 이미지 삭제")
def del_product_review_photo(review_id: int,
                             session: Session = Depends(db.session),
                             member: MemberToken = Depends(token_user)):
    data = ProductReview.get(session, id=review_id, customer_id=member.id)
    if not data:
        raise exc.NotFoundDataEx

    session.query(ProductReviewPhoto).filter(ProductReviewPhoto.product_review_id == review_id).delete()
    session.commit()

    return Success()


def add_text(default_price, selling_price, inventory=None):
    text = ""
    if default_price > selling_price:
        value = '{:,.0f}'.format(default_price - selling_price)
        text = f"(-{value}원)"
    elif default_price < selling_price:
        value = '{:,.0f}'.format(selling_price - default_price)
        text = f"(+{value}원)"
    if inventory:
        if inventory > 0:
            text = text + f" ({inventory}개 남음)"
        else:
            text = text + f" (0개 남음)"

    return text


@router.get("/option/{option_id}", response_model=DataOptions, name="상품옵션 정보")
def get_product(option_id: int,
                store_code: str,
                session: Session = Depends(db.session),
                user: MemberToken = Depends(token_user)):
    opt = ProductOption.get(session=session, id=option_id)
    if not opt:
        raise exc.NotFoundDataEx

    store = Store.get(session, code=store_code)
    original_store = store
    dupl_target = None
    if store.dupl_store:
        dupl_target = Store.get(session, code=store.dupl_store)

    if dupl_target:
        store = dupl_target

    sp = StoreProduct.get(session, store_code=store.code, product_id=opt.product_id)
    if not sp:
        raise exc.NotFoundDataEx

    data = DataOptions.from_orm(opt)
    if sp.variation != 0:
        data.selling_price = data.selling_price + sp.variation

    return data


@router.post("/{product_id}/qna", response_model=Success, name="상품 문의 등록")
def qna(product_id: int,
        indata: AddProductQna,
        session: Session = Depends(db.session),
        user: MemberToken = Depends(token_user)):
    pq = ProductQna()
    pq.title = indata.title
    pq.contents = indata.contents
    pq.product_id = product_id
    pq.status = "R"
    pq.store_code = indata.store_code
    pq.customer_id = user.id
    session.add(pq)
    session.commit()

    return Success()
