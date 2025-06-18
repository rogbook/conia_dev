from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Security, UploadFile, File, Query, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import MemberCompany, Dept, MemberWorker
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, CreatedID
from app.models.user.company import CorpType, DataCompany, ModCompany, AddDept, DataDept, UpdateDept, ListCompany
from app.utils.common_utils import extensions_check, get_extensions
from app.utils.date_utils import D
from app.utils.jwt import token_user
from app.utils.aws import S3
from app.common.consts import AWS_S3_BUCKET_IMG, AWS_S3_BUCKET_IMG_HOST

router = APIRouter(prefix='/company')


@router.post("", response_model=CreatedID, name="회사 등록")
def register_company(member_id: int = Form(description="회원 아이디"),
                     corp_type: CorpType = Form(description="사업자 종류 (개인(P),법인(B),개인사업자(PB),개인사업자간이과세(PBS))"),
                     corp_number: Optional[str] = Form(default=None, description="법인번호"),
                     tax_email: EmailStr = Form(default=None, description="계산서 이메일"),
                     bank: str = Form(default=None, description="은행"),
                     account: str = Form(default=None, description="계좌번호"),
                     bank_user: str = Form(default=None, description="예금주"),
                     name: Optional[str] = Form(default=None, description="회사명"),
                     ceo: Optional[str] = Form(default=None, description="대표자명"),
                     reg_no: Optional[str] = Form(default=None, description="사업자등록번호"),
                     biz_type: Optional[str] = Form(default=None, description="업태"),
                     biz_item: Optional[str] = Form(default=None, description="업종"),
                     zipcode: Optional[str] = Form(default=None, description="우편번호"),
                     address: Optional[str] = Form(default=None, description="주소"),
                     address_detail: Optional[str] = Form(default=None, description="주소상세"),
                     phone: Optional[str] = Form(default=None, description="대표자 전화번호"),
                     mobile: Optional[str] = Form(default=None, description="대표자 휴대전화"),
                     manager_name: Optional[str] = Form(default=None, description="담당자명"),
                     manager_phone: Optional[str] = Form(default=None, description="담당자 전화번호"),
                     manager_mobile: Optional[str] = Form(default=None, description="담당자 휴대전화"),
                     manager_email: Optional[str] = Form(default=None, description="담당자 이메일"),
                     settlement_name: Optional[str] = Form(default=None, description="정산 담당자명"),
                     settlement_phone: Optional[str] = Form(default=None, description="정산 담당자 전화번호"),
                     settlement_mobile: Optional[str] = Form(default=None, description="정산 담당자 휴대전화"),
                     settlement_email: Optional[str] = Form(default=None, description="정산 담당자 이메일"),
                     cs_name: Optional[str] = Form(default=None, description="CS 담당자명"),
                     cs_phone: Optional[str] = Form(default=None, description="CS 담당자 전화번호"),
                     cs_mobile: Optional[str] = Form(default=None, description="CS 담당자 휴대전화"),
                     cs_email: Optional[str] = Form(default=None, description="CS 담당자 이메일"),
                     network_reg_no: Optional[str] = Form(default=None, description="통신판매업 신고번호"),
                     photo_reg: Optional[UploadFile] = File(default=None, description="사업자 등록증 이미지 파일"),
                     photo_bank: Optional[UploadFile] = File(default=None, description="통장 사본 이미지 파일"),
                     session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=[])):
    member_company = MemberCompany.get(session=session, member_id=member_id)
    if member_company:
        # 1계정 1회사 정책(변경 가능)
        raise exc.AlreadyDataEx

    if user.admin != 'Y' and member_id != user.id:
        if "write:company" not in user.scopes:
            raise exc.PermissionEx

    if (photo_reg and not extensions_check(photo_reg.filename)) or (photo_bank and not extensions_check(photo_bank.filename)):
        raise exc.NotAllowedFileEx

    photo_reg_url = ""
    photo_bank_url = ""

    s3 = S3()
    if photo_reg:
        file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{get_extensions(photo_reg.filename)}"
        s3.upload_file(photo_reg, AWS_S3_BUCKET_IMG, 'company/reg/', file_name)
        photo_reg_url: str = f"{AWS_S3_BUCKET_IMG_HOST}company/reg/{file_name}"

    if photo_bank:
        file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{get_extensions(photo_bank.filename)}"
        s3.upload_file(photo_bank, AWS_S3_BUCKET_IMG, 'company/bank/', file_name)
        photo_bank_url: str = f"{AWS_S3_BUCKET_IMG_HOST}company/bank/{file_name}"

    indata_dict = {
        "member_id": member_id,
        "corp_type": corp_type,
        "tax_email": tax_email,
        "bank": bank,
        "account": account,
        "bank_user": bank_user,
        "name": name,
        "ceo": ceo,
        "reg_no": reg_no,
        "biz_type": biz_type,
        "biz_item": biz_item,
        "zipcode": zipcode,
        "address": address,
        "address_detail": address_detail,
        "phone": phone,
        "mobile": mobile,
        "manager_name": manager_name,
        "manager_phone": manager_phone,
        "manager_mobile": manager_mobile,
        "manager_email": manager_email,
        "settlement_name": settlement_name,
        "settlement_phone": settlement_phone,
        "settlement_mobile": settlement_mobile,
        "settlement_email": settlement_email,
        "cs_name": cs_name,
        "cs_phone": cs_phone,
        "cs_mobile": cs_mobile,
        "cs_email": cs_email,
        "network_reg_no": network_reg_no,
        "photo_reg": photo_reg_url,
        "photo_bank": photo_bank_url,
    }

    if corp_number:
        indata_dict["corp_number"] = corp_number

    data = MemberCompany.create(session, auto_commit=True, **indata_dict)

    # TODO : 회사 소유 계정에 부서 생성 권한 설정 (해당 회사)

    return CreatedID(id=data.id)


@router.get("", response_model=ListCompany, name="회사 목록")
def list_company(name: Optional[str] = Query(default=None, title="회사명"),
                 member_id: Optional[int] = Query(default=None, title="회원 ID"),
                 offset: int = 0, limit: int = 20,
                 session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:company"])):
    qry = session.query(MemberCompany)

    if name:
        qry = qry.filter(MemberCompany.name.like(f'%{name}%'))

    if member_id:
        qry = qry.filter(MemberCompany.member_id == member_id)

    total = qry.count()
    qry = qry.order_by(MemberCompany.reg_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListCompany(total=total, datas=datas)


@router.get("/me", response_model=DataCompany, name="회사 정보(본인)")
def get_company_me(session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=[])):
    data = MemberCompany.get(session=session, member_id=user.id)
    if not data:
        raise exc.NotFoundDataEx
    return data


@router.get("/{company_id}", response_model=DataCompany, name="회사 정보")
def get_company(company_id: int,
                session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:company"])):
    data = MemberCompany.get(session=session, id=company_id)
    if not data:
        raise exc.NotFoundDataEx
    return data


@router.put("/{company_id}", response_model=Success, name="회사 수정")
def update_company(company_id: int, indata: ModCompany,
                   session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:company"])):
    data: MemberCompany = MemberCompany.get(session=session, id=company_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.put("/{company_id}/photo", response_model=Success, name="회사 수정 (등록증, 통장사본)")
def update_company_photo(company_id: int,
                         photo_reg: Optional[UploadFile] = File(default=None, description="사업자 등록증 이미지 파일"),
                         photo_bank: Optional[UploadFile] = File(default=None, description="통장 사본 이미지 파일"),
                         session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:company"])):
    if not photo_reg and not photo_bank:
        raise exc.BadRequestEx

    if (photo_reg and not extensions_check(photo_reg.filename)) or (photo_bank and not extensions_check(photo_bank.filename)):
        raise exc.NotAllowedFileEx

    data: MemberCompany = MemberCompany.get(session=session, id=company_id)
    if not data:
        raise exc.NotFoundDataEx

    s3 = S3()
    if photo_reg:
        file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{get_extensions(photo_reg.filename)}"
        s3.upload_file(photo_reg, AWS_S3_BUCKET_IMG, 'company/reg/', file_name)
        data.photo_reg = f"{AWS_S3_BUCKET_IMG_HOST}company/reg/{file_name}"

    if photo_bank:
        file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{get_extensions(photo_bank.filename)}"
        s3.upload_file(photo_bank, AWS_S3_BUCKET_IMG, 'company/bank/', file_name)
        data.photo_bank = f"{AWS_S3_BUCKET_IMG_HOST}company/bank/{file_name}"

    session.commit()

    return Success()


@router.post("/{company_id}/dept", response_model=Success, name="회사 부서 등록")
def add_dept(company_id: int, indata: AddDept,
             session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:dept"])):
    data: MemberCompany = MemberCompany.get(session, id=company_id)
    if not data:
        raise exc.NotFoundDataEx

    target_list = user.scopes.get("write:dept")
    if "*" not in target_list and str(company_id) not in target_list:
        raise exc.PermissionEx

    indata_dict = indata.dict()
    indata_dict.update(member_company_id=company_id)

    Dept.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.get("/{company_id}/dept", response_model=List[DataDept], name="회사 부서 목록")
def list_dept(company_id: int,
              session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:dept"])):
    data: MemberCompany = MemberCompany.get(session, id=company_id)
    if not data:
        raise exc.NotFoundDataEx

    target_list = user.scopes.get("read:dept")
    if "*" not in target_list and str(company_id) not in target_list:
        raise exc.PermissionEx

    data_list = Dept.filter(session=session, member_company_id=company_id).all()

    return data_list


@router.put("/{company_id}/dept/{dept_id}", response_model=Success, name="회사 부서 수정")
def update_dept(company_id: int, dept_id: int, indata: UpdateDept,
                session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:dept"])):
    data = dept_check(session, company_id, dept_id)

    target_list = user.scopes.get("write:dept")
    if "*" not in target_list and str(company_id) not in target_list:
        raise exc.PermissionEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/{company_id}/dept/{dept_id}/link", response_model=Success, name="회사 부서 직원 연결")
def worker_mapping(company_id: int, dept_id: int, member_id: int,
                   session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["link:dept"])):
    dept_check(session, company_id, dept_id)

    target_list = user.scopes.get("link:dept")
    if "*" not in target_list and str(company_id) not in target_list:
        raise exc.PermissionEx

    mapping_data = {
        "member_company_id": company_id,
        "dept_id": dept_id,
        "member_id": member_id
    }
    MemberWorker.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/{company_id}/dept/{dept_id}/link", response_model=Success, name="회사 부서 직원 연결 해제")
def worker_delete(company_id: int, dept_id: int, member_id: int,
                  session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["link:dept"])):
    dept_check(session, company_id, dept_id)

    target_list = user.scopes.get("link:dept")
    if "*" not in target_list and str(company_id) not in target_list:
        raise exc.PermissionEx

    mapping_data = {
        "member_company_id": company_id,
        "dept_id": dept_id,
        "member_id": member_id
    }
    MemberWorker.filter(session=session, **mapping_data).delete(auto_commit=True)

    return Success()


def dept_check(session: Session, company_id: int, dept_id: int):
    data: Dept = Dept.get(session=session, id=dept_id, member_company_id=company_id)
    if not data:
        raise exc.NotFoundDataEx
    return data
