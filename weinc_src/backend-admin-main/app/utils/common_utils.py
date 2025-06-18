import re
import random
import string
from operator import itemgetter

from fastapi import Request, UploadFile
from typing import List
import json
import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField

from app.utils.date_utils import D
from app.errors import exceptions as exc
from app.database.schema import Store, StoreTheme, StoreThemeProduct


def get_ip(request: Request):
    """
    IP 정보
    :param request:
    :return:
    """
    if "x-forwarded-for" in request.headers.keys():
        return request.headers["x-forwarded-for"]
    else:
        return request.client.host


def to_dict(model, *args, exclude: List = None):
    q_dict = {}
    for c in model.__table__.columns:
        if not args or c.name in args:
            if not exclude or c.name not in exclude:
                q_dict[c.name] = getattr(model, c.name)

    return q_dict


def list_to_dict(data_list, *args, exclude: List = None):
    res = []
    for row in data_list:
        q_dict = {}
        for c in row.__table__.columns:
            if not args or c.name in args:
                if not exclude or c.name not in exclude:
                    q_dict[c.name] = getattr(row, c.name)
        res.append(q_dict)

    return res


def make_tree(data):
    """
    트리 구조 데이터 생성
    :param data:
    :return:
    """
    nodes = {}
    for i in data:
        idx, parent_idx = i['id'], i['pid']
        nodes[idx] = i

    forest = []
    for i in data:
        idx, parent_idx = i['id'], i['pid']
        node = nodes[idx]

        if parent_idx is None:
            parent_idx = idx

        if idx == parent_idx:
            forest.append(node)
            forest.sort(key=itemgetter('sort', 'id'))
        else:
            parent = nodes.get(parent_idx, None)
            if parent:
                if 'sub' not in parent:
                    parent['sub'] = []
                sub = parent['sub']
                sub.append(node)
                sub.sort(key=itemgetter('sort', 'id'))
            else:
                forest.append(node)
                forest.sort(key=itemgetter('sort', 'id'))
    return forest


def order_numbering():
    """
    주문번호 생성
    :return:
    """
    now: str = D.yyyymmdd()
    rand_num: int = random.randint(0, 100000000)
    return f"{now}{str(rand_num).zfill(8)}"


def extensions_check(filename: str):
    """
    업로드 파일 확장자 검사
    :param filename:
    :return:
    """
    allowed_extensions = {'png', 'jpg', 'jpeg', 'ico', 'svg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_extensions(filename: str):
    """
    파일 확장자
    :param filename:
    :return:
    """
    return filename.rsplit('.', 1)[1].lower()


def extensions(file: UploadFile):
    """
    업로드 파일 확장자 검사
    :param file:
    :return:
    """
    allowed_extensions = {'png', 'jpg', 'jpeg', 'ico', 'svg', 'gif'}
    if '.' in file.filename:
        file_extensions = file.filename.rsplit('.', 1)[1].lower()
        if file_extensions in allowed_extensions:
            return file_extensions
        else:
            raise exc.NotAllowedFileEx
    else:
        raise exc.NotAllowedFileEx


def log_msg(msg_type: str, data):
    """
    Log 데이터 Json dump
    :param msg_type:
    :param data:
    :return:
    """
    json_data = {
        "type": msg_type,
        "data": data
    }
    return json.dumps(json_data, ensure_ascii=False, default=str)


def as_form(cls: Type[BaseModel]):
    """
    Pydantic with FastAPI forms [Decorator]
    :param cls:
    :return:
    """
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        new_parameters.append(
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.required else Form(model_field.default),
                annotation=model_field.outer_type_,
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls


def delete_layout_product(session, store_code, prd_id):
    """
    상점 레이아웃 데이터에서 상품 삭제
    :param session:
    :param store_code:
    :param prd_id:
    :return:
    """
    store = Store.get(session, code=store_code)
    if store.layout:
        layout = json.loads(store.layout)
        if layout:
            for row in layout:
                if 'column' in row['type']:
                    for col in row['columns']:
                        if col['type'] == 'product':
                            if prd_id == int(col['id']):
                                row['columns'].remove(col)
            store.update(session, True, layout=json.dumps(layout, ensure_ascii=False))

    themes: List[StoreTheme] = StoreTheme.filter(session, store_code=store_code).all()
    for theme in themes:
        StoreThemeProduct.filter(session, store_theme_id=theme.id, product_id=prd_id).delete(True)
        if theme.layout:
            layout = json.loads(theme.layout)
            if layout:
                for row in layout:
                    if 'column' in row['type']:
                        for col in row['columns']:
                            if col['type'] == 'product':
                                if prd_id == int(col['id']):
                                    row['columns'].remove(col)
                theme.update(session, True, layout=json.dumps(layout, ensure_ascii=False))


def generate_random_string(length):
    letters = string.ascii_letters  # 알파벳 (소문자 및 대문자)
    numbers = string.digits  # 숫자
    all_characters = letters + numbers  # 모든 문자

    random_string = ''.join(random.choice(all_characters) for _ in range(length))
    return random_string


def generate_random_string_num(length):
    numbers = string.digits  # 숫자
    all_characters = numbers  # 모든 문자

    random_string = ''.join(random.choice(all_characters) for _ in range(length))
    return random_string


def is_valid_email(email):
    # 이메일 유효성 검사 정규 표현식
    email_regex = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    return re.match(email_regex, email) is not None


def is_valid_phone_number(phone_number):
    # 휴대폰 번호 유효성 검사 정규 표현식
    phone_regex = re.compile(
        r"^(010|011|016|017|018|019)-?\d{3,4}-?\d{4}$"
    )
    return re.match(phone_regex, phone_number) is not None
