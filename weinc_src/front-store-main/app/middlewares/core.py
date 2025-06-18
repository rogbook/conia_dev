import re
import time
from starlette.requests import Request
import sqlalchemy.exc
import pymysql.err
from datetime import timedelta

from jose import jwt, ExpiredSignatureError
from starlette.responses import JSONResponse, RedirectResponse

from app.common.consts import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX

from app.database.schema import SettingValue
from app.models.auth import MemberToken

from app.utils.common_utils import get_user_device_type
from app.utils.date_utils import D
from app.utils.log import api_logger, analytics
from app.utils.templates import templates
from app.utils.jwt import create_token

from app.errors.exceptions import SqlFailureEx, APIException, ViewNotFoundEx, StatusCode
import traceback


async def access_control(request: Request, call_next):
    access_token = ''
    refresh_token = ''
    request.state.req_time = D.datetime()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.user_agent = None
    request.state.service = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies
    request.state.user_agent = headers.get("user-agent")
    request.state.device = get_user_device_type(headers.get("user-agent"))

    if "access_token" in cookies.keys():
        if "Bearer" in cookies.get("access_token"):
            access_token = cookies.get("access_token").replace("Bearer ", "")
            try:
                payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
                request.state.user = MemberToken(**payload)
            except ExpiredSignatureError:
                access_token, refresh_token = refresh_token_check(request, cookies)
            except Exception:
                pass

    url = request.url.path
    if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
        response = await call_next(request)
        if url != "/":
            api_logger(request=request, response=response)
        return response

    if url.startswith("/api"):
        try:
            response = await call_next(request)
            api_logger(request, response)
        except Exception as e:
            print(f"### ERROR : {e}")
            print(traceback.format_exc())
            error = await exception_handler(e)
            error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
            response = JSONResponse(status_code=error.status_code, content=error_dict)
            api_logger(request=request, error=error)
    else:
        try:
            response = await call_next(request)
            if response.status_code == 404 and url.find(".") == -1:
                raise ViewNotFoundEx
            # if response.status_code == 422 and url.find(".") == -1:
            #     raise BadRequestEx
            api_logger(request, response)

            if request.path_params.get('store_code'):
                analytics_data = {
                    "store_code": request.path_params.get('store_code'),
                    "customer_id": request.state.user.id if request.state.user else None,
                    "host": request.url.hostname,
                    "path": request.url.path,
                    "query": request.url.query,
                    "ip": request.state.ip
                }
                analytics("store-view", analytics_data)
        except Exception as e:
            print(f"### ERROR : {e}")
            # print(traceback.format_exc())
            error = await exception_handler(e)
            context_data = dict(
                request=request,
                title=error.code,
                code=error.code,
                msg=error.msg,
                detail=error.detail,
            )
            if error.code in ["AUTH0004"]:
                store_code = url.split('/')[1]
                response = RedirectResponse(f'/{store_code}/auth/login?referer={request.url}')
                token_delete(response)
            elif error.code in ["AUTH0005"]:
                response = RedirectResponse(request.url)
                access_token, refresh_token = refresh_token_check(request, cookies)
                response.set_cookie('access_token', access_token, httponly=True, expires=3600*24*365*10)
                response.set_cookie('refresh_token', refresh_token, httponly=True, expires=3600*24*365*10)
            elif error.code in ["AUTH0011"]:
                store_code = url.split('/')[1]
                response = RedirectResponse(f'/{store_code}')
                token_delete(response)
            elif error.code in ["4041"]:
                response = templates.TemplateResponse("404-illustration.html", context=context_data, status_code=error.status_code)
            else:
                response = templates.TemplateResponse("error-illustration.html", context=context_data, status_code=error.status_code)

            api_logger(request=request, error=error)

            if error.status_code == StatusCode.HTTP_500:
                await send_error(error, request)

    if access_token and refresh_token:
        response.set_cookie('access_token', access_token, httponly=True, expires=3600*24*365*10)
        response.set_cookie('refresh_token', refresh_token, httponly=True, expires=3600*24*365*10)

    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def exception_handler(error: Exception):
    if isinstance(error, sqlalchemy.exc.OperationalError):
        error = SqlFailureEx(ex=error)
    if isinstance(error, pymysql.err.Error):
        error = SqlFailureEx(ex=error)
    if not isinstance(error, APIException):
        error = APIException(ex=error, msg="Server Error", detail=str(error))
    return error


def token_delete(response):
    response.set_cookie('access_token', '', httponly=True)
    response.set_cookie('refresh_token', '', httponly=True)


async def send_error(error, request):
    try:
        import telegram

        token_data = SettingValue.get(type='telegram_alert_api_token')
        room_data = SettingValue.get(type='telegram_alert_room')

        msg = f"""V3 상점 에러
CODE : {error.code} 
EX : {error.ex.args} 
IP : {request.state.ip}
URL : {request.url} """

        bot = telegram.Bot(token=token_data.value)
        await bot.sendMessage(room_data.value, text=msg)
    except:
        pass


def refresh_token_check(request, cookies):
    access_token = ''
    refresh_token = ''

    if "refresh_token" in cookies.keys():
        if "Bearer" in cookies.get("refresh_token"):
            try:
                refresh_token = cookies.get("refresh_token").replace("Bearer ", "")
                payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
                request.state.user = MemberToken(**payload)
                member = MemberToken(**payload)

                access_token = create_token(member.dict(), timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
                refresh_token = create_token(member.dict(), timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
            except:
                pass

    return access_token, refresh_token
