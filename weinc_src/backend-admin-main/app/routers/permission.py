from typing import Union, List, Optional
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Permission, Member, Dept, Class, MemberPermission, DeptPermission, ClassPermission, \
    MemberClass, MemberWorker

from app.models.common import Success
from app.models.permission import DataPermission
from app.models.auth import MemberToken


router = APIRouter(prefix='/permission')


@router.get("", name="권한 목록")
def list_permission(member_id: Optional[int] = None,
                    dept_id: Optional[int] = None,
                    class_code: Optional[str] = None,
                    session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=[])):
    """
    **member_id, dept_id, class_code** 조건은 1개만 선택 가능
    """
    parameter_check_count = 0
    if member_id: parameter_check_count += 1
    if dept_id: parameter_check_count += 1
    if class_code: parameter_check_count += 1

    if parameter_check_count > 1:
        raise exc.BadRequestEx(reason="검색 조건(member_id, dept_id, class_code)은 1가지만 선택 되어야 합니다.")

    if member_id:
        res = {}
        mc = MemberClass.filter(session, member_id=member_id).all()
        if mc:
            res['Class'] = []
            for row in mc:
                data_list = session.query(ClassPermission.permission_code, Permission.name, ClassPermission.target).join(
                    ClassPermission, Permission.code == ClassPermission.permission_code).filter(
                    ClassPermission.class_code == row.class_code).all()
                permissions = []
                for pm in data_list:
                    permissions.append(pm)

                res['Class'].append({"class_code": row.class_code, "permissions": permissions})

            if not res['Class']:
                del res['Class']


        mw = session.query(MemberWorker).filter(MemberWorker.member_id == member_id).all()
        if mw:
            res['Dept'] = []
            for row in mw:
                data_list = session.query(DeptPermission.permission_code, Permission.name, DeptPermission.target).join(
                    DeptPermission, Permission.code == DeptPermission.permission_code).filter(
                    DeptPermission.dept_id == row.dept_id).all()
                permissions = []
                for pm in data_list:
                    permissions.append(pm)
                if permissions:
                    res['Dept'].append({
                        "company_id": row.member_company_id,
                        "company_name": row.member_company.name,
                        "dept_id": row.dept_id,
                        "dept_name": row.dept.name,
                        "permissions": permissions
                    })
                if not res['Dept']:
                    del res['Dept']

        mp = session.query(MemberPermission.permission_code, Permission.name, MemberPermission.target, MemberPermission.exclude).join(MemberPermission, Permission.code == MemberPermission.permission_code).filter(
            MemberPermission.member_id == member_id).all()

        if mp:
            res['Member'] = []
            for row in mp:
                res['Member'].append(row)

        return res

    if dept_id:
        qry = session.query(DeptPermission.permission_code, Permission.name, DeptPermission.target).join(DeptPermission, Permission.code == DeptPermission.permission_code).filter(
            DeptPermission.dept_id == dept_id)
    elif class_code:
        qry = session.query(ClassPermission.permission_code, Permission.name, ClassPermission.target).join(ClassPermission, Permission.code == ClassPermission.permission_code).filter(
            ClassPermission.class_code == class_code)
    else:
        qry = session.query(Permission)

    data_list = qry.all()

    return data_list


@router.post("/{code}/link", response_model=Success, name="권한 연결")
def class_link(code: str, target: str, member_id: Optional[int] = None, dept_id: Optional[int] = None, class_code: Optional[str] = None,
               session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=["link:permission"])):
    data = Permission.get(session=session, code=code)
    if not data:
        raise exc.NotFoundDataEx

    if member_id:
        if not Member.get(session=session, id=member_id):
            raise exc.NotFoundDataEx

        mapping_data = {
            "permission_code": code,
            "target": target,
            "member_id": member_id
        }
        MemberPermission.create(session=session, auto_commit=True, **mapping_data)

    if dept_id:
        if not Dept.get(session=session, id=dept_id):
            raise exc.NotFoundDataEx

        mapping_data = {
            "permission_code": code,
            "target": target,
            "dept_id": dept_id
        }
        DeptPermission.create(session=session, auto_commit=True, **mapping_data)

    if class_code:
        if not Class.get(session=session, code=class_code):
            raise exc.NotFoundDataEx

        mapping_data = {
            "permission_code": code,
            "target": target,
            "class_code": class_code
        }
        ClassPermission.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/{code}/link", response_model=Success, name="권한 연결 해제")
def class_unlink(code: str, member_id: Optional[int] = None, dept_id: Optional[int] = None, class_code: Optional[str] = None,
                 session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=["link:permission"])):
    data = Permission.get(session=session, code=code)
    if not data:
        raise exc.NotFoundDataEx

    if member_id:
        if not Member.get(session=session, id=member_id):
            raise exc.NotFoundDataEx

        mapping_data = {
            "permission_code": code,
            "member_id": member_id
        }
        MemberPermission.filter(session=session, **mapping_data).delete(auto_commit=True)

    if dept_id:
        if not Dept.get(session=session, id=dept_id):
            raise exc.NotFoundDataEx

        mapping_data = {
            "permission_code": code,
            "dept_id": dept_id
        }
        DeptPermission.filter(session=session, **mapping_data).delete(auto_commit=True)

    if class_code:
        if not Class.get(session=session, code=class_code):
            raise exc.NotFoundDataEx

        mapping_data = {
            "permission_code": code,
            "class_code": class_code
        }
        ClassPermission.filter(session=session, **mapping_data).delete(auto_commit=True)

    return Success()


@router.put("/{code}/{member_id}/exclude", response_model=Success, name="개인 권한 제외 (exclude)")
def exclude_permission(code: str, member_id: int, exclude: str,
                 session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=["link:permission"])):
    data = Permission.get(session=session, code=code)
    if not data:
        raise exc.NotFoundDataEx

    if not Member.get(session=session, id=member_id):
        raise exc.NotFoundDataEx

    member_permission = MemberPermission.get(session=session, permission_code=code, member_id=member_id)
    mod_data = {
        "exclude": exclude
    }
    change_data = member_permission.update_optional(session=session, auto_commit=True, **mod_data)

    return Success()
