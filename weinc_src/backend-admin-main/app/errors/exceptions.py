from fastapi import status


class StatusCode:
    HTTP_500 = status.HTTP_500_INTERNAL_SERVER_ERROR
    HTTP_400 = status.HTTP_400_BAD_REQUEST
    HTTP_401 = status.HTTP_401_UNAUTHORIZED
    HTTP_403 = status.HTTP_403_FORBIDDEN
    HTTP_404 = status.HTTP_404_NOT_FOUND
    HTTP_405 = status.HTTP_405_METHOD_NOT_ALLOWED


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str
    ex: Exception

    def __init__(
            self,
            *,
            status_code: int = StatusCode.HTTP_500,
            code: str = "500",
            msg: str = None,
            detail: str = None,
            ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)


class AlreadyUserEx(APIException):
    def __init__(self, user_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"사용 중인 아이디 입니다.",
            detail=f"Already User ID : {user_id}",
            code=f"AUTH{'1'.zfill(4)}",
            ex=ex,
        )


class NotFoundUserEx(APIException):
    def __init__(self, user_id: str = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"해당 유저를 찾을 수 없습니다.",
            detail=f"Not Found User ID : {user_id}" if user_id else f"Not Found User",
            code=f"AUTH{'2'.zfill(4)}",
            ex=ex,
        )


class NotMatchPWEx(APIException):
    def __init__(self, user_id: int = None, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"패스워드를 확인해 주세요.",
            detail=f"Not Match Password",
            code=f"AUTH{'3'.zfill(4)}",
            ex=ex,
        )


class NotAuthorized(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"로그인이 필요한 서비스 입니다.",
            detail="Authorization Required",
            code=f"AUTH{'4'.zfill(4)}",
            ex=ex,
        )


class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"세션이 만료되어 로그아웃 되었습니다.",
            detail="Token Expired",
            code=f"AUTH{'5'.zfill(4)}",
            ex=ex,
        )


class TokenDecodeEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"비정상적인 접근입니다.",
            detail="Token has been compromised.",
            code=f"AUTH{'6'.zfill(4)}",
            ex=ex,
        )


class InvalidIpEx(APIException):
    def __init__(self, ip: str, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"{ip}는 올바른 IP 가 아닙니다.",
            detail=f"invalid IP : {ip}",
            code=f"AUTH{'7'.zfill(4)}",
            ex=ex,
        )


class RequestCountEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"허용된 요청 횟수를 초과하였습니다.",
            detail="Overed count of request",
            code=f"AUTH{'8'.zfill(4)}",
            ex=ex,
        )


class RequestNotYetEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"지금은 요청할 수 없습니다.",
            detail="Cannot request at this time.",
            code=f"AUTH{'9'.zfill(4)}",
            ex=ex,
        )


class CertFailEx(APIException):
    def __init__(self, category: str = "0", ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"인증에 실패하였습니다.",
            detail="Cert failed.",
            code=f"AUTH{'10'.zfill(4)}_{category}",
            ex=ex,
        )


class NotAvailableEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"서비스를 이용할 수 없습니다.",
            detail="Not available for service",
            code=f"AUTH{'11'.zfill(4)}",
            ex=ex,
        )


class SqlFailureEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"이 에러는 서버측 에러 입니다. 자동으로 리포팅 되며, 빠르게 수정하겠습니다.",
            detail="Internal Server Error [Database]",
            code=f"ERROR{'1'.zfill(4)}",
            ex=ex,
        )


class PermissionEx(APIException):
    def __init__(self):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg=f"해당 권한을 가지고 있지 않습니다.",
            detail="Permission denied",
            code=f"{StatusCode.HTTP_403}{'1'.zfill(4)}"
        )


class AlreadyDataEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"이미 등록된 데이터 입니다.",
            detail="Data already registered.",
            code=f"DATA{'1'.zfill(4)}",
            ex=ex,
        )


class NotFoundDataEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_404,
            msg=f"데이터 찾을 수 없습니다.",
            detail="Data not found.",
            code=f"DATA{'2'.zfill(4)}",
            ex=ex,
        )


class NotChangeDataEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"데이터 변경 사항이 없습니다.",
            detail="Data not changed.",
            code=f"DATA{'3'.zfill(4)}",
            ex=ex,
        )


class NotAllowedFileEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"지원하지 않는 파일 확장자 입니다.",
            detail="Not allowed file extensions.",
            code=f"DATA{'4'.zfill(4)}",
            ex=ex,
        )


class BadRequestEx(APIException):
    def __init__(self, reason: str = ""):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            msg=f"잘못된 요청입니다. {reason}",
            detail="Bad Request.",
            code=f"DATA{'5'.zfill(4)}",
        )


class PgFailEx(APIException):
    def __init__(self, msg: str = "", code: str = ""):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"결제 API 오류",
            detail=msg,
            code=f"CODE_{code}",
        )


class ProcessFailEx(APIException):
    def __init__(self, msg: str = "", code: str = ""):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"처리에 실패하였습니다.",
            detail=msg,
            code=f"CODE_{code}",
        )


class ReadyConfirmEx(APIException):
    def __init__(self):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg=f"승인 대기중 입니다.",
            detail="Ready for confirm",
            code=f"{StatusCode.HTTP_403}{'2'.zfill(4)}"
        )


class ReadyConfirmUniqueEx(APIException):
    def __init__(self):
        super().__init__(
            status_code=StatusCode.HTTP_403,
            msg=f"승인 대기중 입니다.",
            detail="Ready for confirm",
            code=f"{StatusCode.HTTP_403}{'3'.zfill(4)}"
        )

class NotMatchSnsEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            msg=f"해당 소셜 계정과 연결된 사용자가 없습니다.",
            detail="Not match sns account",
            code=f"AUTH{'12'.zfill(4)}",
            ex=ex,
        )


# 샘플용
class Ex(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            msg=f"",
            detail="",
            code=f"CODE{'2'.zfill(4)}",
            ex=ex,
        )
