from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import ShippingInfo, ShippingCost, ShippingArea, ShippingAreaDetail

from app.models.common import Success, CreatedID
from app.models.product.shipping import *
from app.models.auth import MemberToken

router = APIRouter(prefix='/product/shipping-info')


@router.post("", response_model=CreatedID, name="배송정보 등록")
def add_shipping_info(indata: AddShippingInfo,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    indata_dict = indata.dict()
    data = ShippingInfo.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("", response_model=List[DataShippingInfo], name="배송정보 목록")
def list_shipping_info(member_id: Optional[int] = Query(default=None, description="PA id"),
                       session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:shipping"])):
    
    if member_id:
        data_list = ShippingInfo.filter(session=session, member_id=member_id).all()
    else:
        data_list = ShippingInfo.filter(session=session).all()

    return data_list


@router.get("/{info_id}", response_model=DataShippingInfo, name="배송정보")
def get_shipping_info(info_id: int,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:shipping"])):
    data = ShippingInfo.get(session, id=info_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/{info_id}", response_model=Success, name="배송정보 수정")
def mod_shipping_info(info_id: int, indata: ModShippingInfo,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingInfo = ShippingInfo.get(session=session, id=info_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/{info_id}/cost", response_model=Success, name="배송비 등록")
def add_shipping_cost(info_id: int, indata: List[AddShippingCost],
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingInfo = ShippingInfo.get(session=session, id=info_id)
    if not data:
        raise exc.NotFoundDataEx

    for c in indata:
        indata_dict = c.dict()
        indata_dict.update(shipping_info_id=info_id)
        ShippingCost.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.delete("/{info_id}/cost", response_model=Success, name="배송비 삭제")
def del_shipping_cost(info_id: int,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    ShippingCost.filter(session=session, shipping_info_id=info_id).delete(auto_commit=True)

    return Success()


@router.post("/{info_id}/cost/{cost_id}/area", response_model=Success, name="배송비 지역 등록")
def add_shipping_area(info_id: int, cost_id: int, indata: AddShippingArea,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingCost = ShippingCost.get(session=session, id=cost_id, shipping_info_id=info_id)
    if not data:
        raise exc.NotFoundDataEx

    indata_dict = indata.dict()
    ShippingArea.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.put("/{info_id}/cost/{cost_id}/area/{area_id}", response_model=Success, name="배송비 지역 수정")
def mod_shipping_area(info_id: int, cost_id: int, area_id: int, indata: ModShippingArea,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingArea = ShippingArea.get(session=session, id=area_id, shipping_cost_id=cost_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.delete("/{info_id}/cost/{cost_id}/area/{area_id}", response_model=Success, name="배송비 지역 삭제")
def del_shipping_area(info_id: int, cost_id: int, area_id: int,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingArea = ShippingArea.get(session=session, id=area_id, shipping_cost_id=cost_id)
    if not data:
        raise exc.NotFoundDataEx

    mapping_data = {
        "id": area_id,
        "shipping_cost_id": cost_id,
    }
    ShippingArea.filter(session=session, **mapping_data).delete(auto_commit=True)

    return Success()


@router.post("/{info_id}/cost/{cost_id}/area/{area_id}/detail", response_model=Success, name="배송비 지역 상세 등록")
def add_shipping_area_detail(info_id: int, cost_id: int, area_id: int, indata: AddShippingAreaDetail,
                             session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingArea = ShippingArea.get(session=session, id=area_id, shipping_cost_id=cost_id)
    if not data:
        raise exc.NotFoundDataEx

    indata_dict = indata.dict()
    ShippingAreaDetail.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.put("/{info_id}/cost/{cost_id}/area/{area_id}/detail/{detail_id}", response_model=Success, name="배송비 지역 상세 수정")
def mod_shipping_area_detail(info_id: int, cost_id: int, area_id: int, detail_id: int, indata: ModShippingAreaDetail,
                             session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingAreaDetail = ShippingAreaDetail.get(session=session, id=detail_id, shipping_area_id=area_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.delete("/{info_id}/cost/{cost_id}/area/{area_id}/detail/{detail_id}", response_model=Success, name="배송비 지역 상세 삭제")
def del_shipping_area_detail(info_id: int, cost_id: int, area_id: int, detail_id: int,
                             session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:shipping"])):
    data: ShippingAreaDetail = ShippingAreaDetail.get(session=session, id=detail_id, shipping_area_id=area_id)
    if not data:
        raise exc.NotFoundDataEx

    mapping_data = {
        "id": area_id,
        "shipping_area_id": area_id,
    }
    ShippingAreaDetail.filter(session=session, **mapping_data).delete(auto_commit=True)

    return Success()
