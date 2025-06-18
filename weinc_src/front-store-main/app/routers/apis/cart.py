from typing import List

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.utils.common_utils import check_product_state, get_ip
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Cart, ProductOption

from app.models.common import Success
from app.models.cart import *
from app.models.auth import MemberToken
from app.utils.log import analytics

router = APIRouter(prefix='/cart')


@router.post("", response_model=Success, name="장바구니 상품 등록")
def add_cart(indata: List[AddCart], req: Request,
             store_code: str = Query(title="상점 코드"),
             session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    for row in indata:
        po = ProductOption.get(session, id=row.product_option_id)

        # 상품 상태 검증
        # 재고, 상태, 진열 상태
        if not check_product_state(session, po.product_id, po.id, store_code):
            raise exc.NotFoundDataEx

        item = Cart.get(session, product_option_id=row.product_option_id, customer_id=user.id, store_code=store_code)

        if item:
            item.count = item.count + row.count
        else:
            # 배송 상품 장바구니
            if po.product.type[0] == "D":
                indata_dict = row.dict()
                indata_dict.update(customer_id=user.id)
                indata_dict.update(store_code=store_code)
                indata_dict.update(type=po.product.type[0])
                Cart.create(session, **indata_dict)
            # 미배송 상품 장바구니
            else:
                item: Cart = Cart.filter(session, type="U", customer_id=user.id, store_code=store_code).first()

                if item and item.product_option.product.member_id != po.product.member_id:
                    if row.force:
                        Cart.filter(session, type="U", customer_id=user.id, store_code=store_code).delete(True)
                    else:
                        raise exc.AlreadyDataEx

                indata_dict = row.dict()
                indata_dict.update(customer_id=user.id)
                indata_dict.update(store_code=store_code)
                indata_dict.update(type=po.product.type[0])
                Cart.create(session, **indata_dict)

        analytics_data = {
            "store_code": store_code,
            "product_id": po.product_id,
            "customer_id": user.id if user else None,
            "ip": get_ip(req)
        }
        analytics("cart-product", analytics_data)

    session.commit()

    return Success()


@router.get("", response_model=List[DataCart], name="장바구니 목록")
def list_cart(session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data_list = Cart.filter(session=session, customer_id=member.id).all()
    return data_list


@router.put("/{cart_id}", response_model=Success, name="장바구니 수정")
def mod_cart(cart_id: int, indata: ModCart,
             session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Cart = Cart.get(session=session, id=cart_id)
    if not data:
        raise exc.NotFoundDataEx

    if indata.count is not None:
        data.count = indata.count

    if indata.checked is not None:
        data.checked = indata.checked

    session.commit()

    return Success()


@router.delete("/{cart_id}", response_model=Success, name="장바구니 삭제")
def del_cart(cart_id: int,
             session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Cart = Cart.get(session=session, id=cart_id)
    if not data:
        raise exc.NotFoundDataEx

    session.delete(data)
    session.commit()

    return Success()
