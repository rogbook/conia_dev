import json
from typing import List

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import ProductOption, Inventory, LogProduct
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import *
from app.models.product.option import *
from app.utils.jwt import token_user
from app.utils.common_utils import log_msg

router = APIRouter(prefix='/product/{product_id}')


@router.post("/option", response_model=Success, name="상품 옵션 등록")
def add_product_option(product_id: int, indata: List[AddProductOption],
                       session: Session = Depends(db.session),
                       user: MemberToken = Security(token_user, scopes=['write:product'])):
    for row in indata:
        indata_dict = row.dict()
        option = ProductOption.create(session, auto_commit=True, product_id=product_id, **indata_dict)

        inven_data = {
            "count": row.count,
            "safe_count": row.safe_count,
            "product_option_id": option.id,
            "use_acc_qty": row.use_acc_qty,
        }
        if row.day_able_count:
            inven_data["day_able_count"] = row.day_able_count
        Inventory.create(session, **inven_data)

        # 로깅
        log_data = LogProductDataIn(action="옵션 등록", product_id=product_id, msg=log_msg("msg", f"옵션 등록 - {json.dumps(indata_dict, ensure_ascii=False, default=str)}"), writer=f"{user.name}:{user.id}")
        LogProduct.create(session, auto_commit=True, **log_data.dict())

    session.commit()

    return Success()


@router.get("/option", response_model=List[DataProductOption], name="상품 옵션 목록")
def list_product_option(product_id: int,
                        session: Session = Depends(db.session),
                        user: MemberToken = Security(token_user, scopes=['read:product'])):
    data_list = ProductOption.filter(session=session, product_id=product_id, status='Y').all()
    return data_list


@router.delete("/option", response_model=Success, name="상품 옵션 삭제")
def del_product_option(product_id: int, option_ids: List[int],
                       session: Session = Depends(db.session),
                       user: MemberToken = Security(token_user, scopes=['write:product'])):
    for row in option_ids:
        ProductOption.filter(session=session, id=row, product_id=product_id).update_q(auto_commit=False, status='D')
    session.commit()

    # 로깅
    log_data = LogProductDataIn(action="옵션 삭제", product_id=product_id, msg=log_msg("msg", f"옵션 삭제 - {option_ids}"), writer=f"{user.name}:{user.id}")
    LogProduct.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.put("/option", response_model=Success, name="상품 옵션 수정")
def mod_product_option(indata: List[ModProductOption],
                       session: Session = Depends(db.session),
                       user: MemberToken = Security(token_user, scopes=['write:product'])):
    for row in indata:
        data: ProductOption = ProductOption.get(session=session, id=row.opt_id)
        change_data = data.update_optional(session=session, auto_commit=True, auto_error=False, **row.dict())
        change_data.insert(0, dict(option_id=row.opt_id))

        if row.count is not None and data.inventory.count != row.count:
            change_data.append(dict(count=dict(before=data.inventory.count, after=row.count)))
            data.inventory.count = row.count
        if row.safe_count is not None and data.inventory.safe_count != row.safe_count:
            change_data.append(dict(safe_count=dict(before=data.inventory.safe_count, after=row.safe_count)))
            data.inventory.safe_count = row.safe_count
        if row.day_able_count is not None and data.inventory.day_able_count != row.day_able_count:
            change_data.append(dict(day_able_count=dict(before=data.inventory.day_able_count, after=row.day_able_count)))
            data.inventory.day_able_count = row.day_able_count
        if row.use_acc_qty is not None and data.inventory.use_acc_qty != row.use_acc_qty:
            change_data.append(dict(use_acc_qty=dict(before=data.inventory.use_acc_qty, after=row.use_acc_qty)))
            data.inventory.use_acc_qty = row.use_acc_qty

        # 로깅
        log_data = LogProductDataIn(action="옵션 수정", product_id=data.product_id, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
        LogProduct.create(session, auto_commit=True, **log_data.dict())

    session.commit()

    return Success()


@router.put("/option/{option_id}/inven", response_model=Success, name="상품 옵션 재고 수정")
def mod_product_option_inventory(product_id: int, option_id: int, indata: ModProductInventory,
                                 session: Session = Depends(db.session),
                                 user: MemberToken = Security(token_user, scopes=['write:product'])):
    data: Inventory = Inventory.get(session=session, product_option_id=option_id)
    if not data:
        raise exc.NotFoundDataEx

    if indata.count:
        change_value = indata.count - data.count

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())
    change_data.insert(0, dict(option_id=option_id))

    # 로깅
    log_data = LogProductDataIn(action="재고 수정", product_id=product_id, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogProduct.create(session, auto_commit=True, **log_data.dict())

    return Success()
