import logging
import os
import time
from starlette.requests import Request
from datetime import datetime, timedelta
from app.database.conn import mongo


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class L(metaclass=SingletonType):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("CONIA_LOG")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('CONIA_LOG [%(levelname)s] %(asctime)s > %(message)s')

        import datetime
        now = datetime.datetime.now()
        import time
        timestamp = time.mktime(now.timetuple())

        dirname = './log'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        # fileHandler = logging.FileHandler(dirname + "/Aries_"+now.strftime("%Y-%m-%d %H:%M:%S")+".log")
        stream_handler = logging.StreamHandler()

        # fileHandler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        # self._logger.addHandler(fileHandler)
        self._logger.addHandler(stream_handler)

    def get_logger(self):
        return self._logger

    def debug(self, msg):
        self._logger.debug(msg)

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)


def api_logger(request: Request, response=None, error=None):
    time_format = "%Y/%m/%d %H:%M:%S"
    t = time.time() - request.state.start
    status_code = error.status_code if error else response.status_code
    user = request.state.user
    error_log = None

    if error:
        if request.state.inspect:
            frame = request.state.inspect
            error_file = frame.f_code.co_filename
            error_func = frame.f_code.co_name
            error_line = frame.f_lineno
        else:
            error_func = error_file = error_line = "UNKNOWN"

        error_log = dict(
            errorFunc=error_func,
            location="{} line in {}".format(str(error_line), error_file),
            raised=str(error.__class__.__name__),
            msg=str(error.msg),
            detail=str(error.detail),
            ex=str(error.ex),
        )

    user_log = dict(
        client=request.state.ip,
        user_agent=request.state.user_agent,
        user=user.id if user and user.id else None,
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        client=user_log,
        errorDetail=error_log,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeUTC=datetime.utcnow().strftime(time_format),
        datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format),
    )

    mongo_col = mongo.store_access
    mongo_col.insert_one(log_dict)


def data_logger(log_dict: dict):
    time_format = "%Y/%m/%d %H:%M:%S"

    log_dict.update(datetimeUTC=datetime.utcnow().strftime(time_format))
    log_dict.update(datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format))

    mongo_log = mongo.api_log
    mongo_log.insert_one(log_dict)


def analytics(target: str, analytics_dict: dict):
    time_format = "%Y/%m/%d %H:%M:%S"

    analytics_dict.update(datetimeUTC=datetime.utcnow().strftime(time_format))
    analytics_dict.update(datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format))

    collection = mongo.collection(target)
    collection.insert_one(analytics_dict)
