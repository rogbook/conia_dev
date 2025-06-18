import time
from starlette.requests import Request
import sqlalchemy.exc
import pymysql.err

from jose import jwt
from starlette.responses import JSONResponse
from starlette.types import Message

from app.common.consts import JWT_SECRET_KEY, JWT_ALGORITHM
from app.models.auth import MemberToken
from app.utils.date_utils import D
from app.utils.log import api_logger

from app.errors.exceptions import SqlFailureEx, APIException, StatusCode
import traceback


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}
    request._receive = receive


async def access_control(request: Request, call_next):
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.user_agent = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    request.state.user_agent = headers.get("user-agent")

    if "authorization" in headers.keys():
        if "Bearer" in headers.get("authorization"):
            access_token = headers.get("Authorization").replace("Bearer ", "")
            try:
                payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
                request.state.user = MemberToken(**payload)
            except Exception as e:
                pass

    try:
        req_body = await request.body()
        await set_body(request, req_body)

        response = await call_next(request)
        api_logger(request, response)
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        api_logger(request=request, error=error)

        if error.status_code == StatusCode.HTTP_500:
            await send_error(error, request, req_body)

    return response


async def exception_handler(error: Exception):
    if error:
        print(error)
    # print(traceback.format_exc())
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureEx(ex=error)
    if isinstance(error, pymysql.err.Error):
        error = SqlFailureEx(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, msg="Server error", detail=str(error))
    return error


async def send_error(error, request, req_body=None):
    try:
        import telegram
        from app.database.schema import SettingValue

        token_data = SettingValue.get(type='telegram_alert_api_token')
        room_data = SettingValue.get(type='telegram_alert_room')

        msg = f"""V3 API 에러
CODE : {error.code} 
EX : {error.ex.args} 
IP : {request.state.ip}
METHOD : {request.method}
BODY : {req_body.decode('utf-8') if req_body else ''}
USER : {request.state.user} 
URL : {request.url} """

        bot = telegram.Bot(token=token_data.value)
        await bot.sendMessage(room_data.value, text=msg)
    except:
        pass
