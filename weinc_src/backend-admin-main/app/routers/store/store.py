from uuid import uuid4

from fastapi import APIRouter, Depends, Query, UploadFile, Request, Security
from sqlalchemy.orm import Session

from app.common.consts import AWS_S3_BUCKET_IMG, AWS_S3_BUCKET_IMG_HOST
from app.database.conn import db
from app.database.schema import Store, MemberMember, LogStore, StoreBoardGroup
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, Exist, CreatedURI, LogStoreDataIn, ListLog
from app.models.store import *
from app.utils.aws import S3
from app.utils.common_utils import get_ip, log_msg, extensions
from app.utils.date_utils import D
from app.utils.jwt import token_user
from app.utils.log import data_logger

router = APIRouter(prefix='/store')


@router.post("", response_model=Success, name="상점 등록")
def add_store(indata: AddStore,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    indata_dict = indata.dict()
    data = Store.create(session, auto_commit=True, **indata_dict)

    # 로깅
    log_data = LogStoreDataIn(action="등록", store_code=data.code, msg=log_msg("msg", "상점 등록"), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    # 이벤트 게시판 자동 생성
    sbg = StoreBoardGroup()
    sbg.name = "이벤트"
    sbg.view_type = "thumbnail"
    sbg.store_code = data.code
    session.add(sbg)
    session.flush()
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="상점 게시판 그룹 생성", store_code=data.code, msg=log_msg("msg", f'대상 - {sbg.id}'), writer=f"system")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("", response_model=ListDataStore, name="상점 목록")
def list_store(title: Optional[str] = Query(default=None, description="상점명"),
               code: Optional[str] = Query(default=None, description="상점 코드"),
               group: Optional[str] = Query(default=None, description="그룹"),
               offset: int = 0, limit: int = 20,
               session: Session = Depends(db.session),
               user: MemberToken = Security(token_user, scopes=['read:store'])):
    qry = session.query(Store)

    if title:
        qry = qry.filter(Store.title.like(f'%{title}%'))

    if code:
        qry = qry.filter(Store.code == code)

    if group:
        qry = qry.filter(Store.group == group)

    total = qry.count()
    qry = qry.order_by(Store.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListDataStore(total=total, datas=data_list)


@router.get("/group", name="상점 그룹 목록")
def get_group(session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['read:store'])):
    qry = session.query(Store.group).filter(Store.group != None)

    data_list = qry.group_by(Store.group).all()

    result = []
    for data in data_list:
        result.append(data.group)

    return result


@router.post("/photo", response_model=CreatedURI, name="상점 레이아웃용 사진 등록")
def add_layout_photo(file: UploadFile, req: Request,
                     ext: str = Depends(extensions),
                     user: MemberToken = Security(token_user, scopes=['write:store'])):
    s3 = S3()

    file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{ext}"
    s3.upload_file(file, AWS_S3_BUCKET_IMG, 'store/layout/', file_name)
    url: str = f"{AWS_S3_BUCKET_IMG_HOST}store/layout/{file_name}"

    log_dict = dict(
        category="store",
        action="add file",
        type="layout_photo",
        ip=get_ip(req),
        user=user.id,
        user_name=user.name,
        data=url,
    )
    data_logger(log_dict)

    return CreatedURI(uri=url)


@router.post("/logo", response_model=CreatedURI, name="상점 로고 이미지 등록")
def add_logo(file: UploadFile, req: Request,
             store_code: str = Query(title="상점 코드"),
             logo_type: EnumLogoType = Query(title="이미지 타입"),
             session: Session = Depends(db.session),
             ext: str = Depends(extensions),
             user: MemberToken = Security(token_user, scopes=['write:store'])):
    store = Store.get(session, code=store_code)
    if not store:
        raise exc.NotFoundDataEx

    s3 = S3()

    file_name = f"{logo_type}-{uuid4().hex[:4]}.{ext}"
    s3.upload_file(file, AWS_S3_BUCKET_IMG, 'store/logo/', file_name)
    url: str = f"{AWS_S3_BUCKET_IMG_HOST}store/logo/{file_name}"

    log_dict = dict(
        category="store",
        action="add file",
        type=f"logo-{logo_type}",
        ip=get_ip(req),
        user=user.id,
        user_name=user.name,
        data=url,
    )
    data_logger(log_dict)

    return CreatedURI(uri=url)


@router.get("/exist", response_model=Exist, name="상점 코드 중복 확인")
def exist_code(code: str,
               session: Session = Depends(db.session)):
    data = Store.get(session, code=code)
    if data:
        return Exist(exist=True)
    return Exist(exist=False)


@router.get("/sub_store", response_model=List[SubStore], name="하위 상점 목록")
def sub_stores(member_id: int, session: Session = Depends(db.session),
               user: MemberToken = Security(token_user, scopes=['write:sub_commission'])):
    sub_members: List[MemberMember] = MemberMember.filter(session, pid=member_id).all()

    result = []

    for sub in sub_members:
        sub_store = Store.get(session, member_id=sub.member_id)
        if sub_store:
            result.append(SubStore(title=sub_store.title, store_code=sub_store.code))

    return result


@router.get("/{store_code}", response_model=DataStore, name="상점 정보")
def get_store(store_code: str,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['read:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/{store_code}", response_model=Success, name="상점 수정")
def mod_store(store_code: str, indata: ModStore,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action="수정", store_code=data.code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/log", response_model=ListLog, name="상점 Log")
def store_log(store_code: str,
              offset: int = 0, limit: int = 20,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['read:store'])):
    qry = session.query(LogStore).filter(LogStore.store_code == store_code, LogStore._del != "Y")

    total = qry.count()
    qry = qry.order_by(LogStore.reg_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListLog(total=total, datas=datas)


@router.put("/{store_code}/copy-setting", response_model=Success, name="상점 설정 복사 요청")
def copy_setting(store_code: str, indata: TargetStore,
                 session: Session = Depends(db.session),
                 user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    target: Store = Store.get(session=session, code=indata.target_store_code)
    if not target:
        raise exc.BadRequestEx(reason='대상이 없습니다.')

    data.status = 'SR'
    data.copy_setting = indata.target_store_code
    session.commit()

    # 로깅
    log_data = LogStoreDataIn(action="수정", store_code=data.code, msg=log_msg("msg", f"설정 복사 요청(대상 : {target.title}[{target.code}])"), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()
