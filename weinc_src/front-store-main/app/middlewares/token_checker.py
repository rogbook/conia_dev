import time
from starlette.requests import Request

from jose import jwt

from app.common.consts import JWT_SECRET_KEY, JWT_ALGORITHM
from app.models.auth import MemberToken
from app.models.member import DataMember
from app.utils.common_utils import to_dict
from app.utils.date_utils import D


def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies

    url = request.url.path

    # if "authorization" in headers.keys():
    #     if "Bearer" in headers.get("authorization"):
    #         access_token = headers.get("Authorization").replace("Bearer ", "")
    #         payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    #         request.state.user = MemberToken(**payload)

    return call_next(request)
