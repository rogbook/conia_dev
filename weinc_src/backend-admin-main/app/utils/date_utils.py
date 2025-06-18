from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import time


class D:
    """
    날짜,시간 관련 유틸
    """
    def __init__(self):
        self.utc_now = datetime.utcnow()
        self.now = datetime.now()

    @classmethod
    def datetime(cls, diff: int = 0) -> datetime:
        return cls().utc_now + timedelta(hours=diff) if diff > 0 else cls().utc_now + timedelta(hours=diff)

    @staticmethod
    def milli_time():
        """
        milli second
        :return:
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def now_str():
        """
        현재 시간
        :return: %Y-%m-%d %H:%M:%S
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def now_str_trim():
        """
        현재 시간
        :return: %Y%m%d%H%M%S
        """
        return datetime.now().strftime('%Y%m%d%H%M%S')

    @staticmethod
    def yyyymmdd():
        """
        현재 시간
        :return: %Y%m%d
        """
        return datetime.now().strftime('%Y%m%d')

    @staticmethod
    def convert_yyyymmdd(target: datetime):
        """
        현재 시간
        :return: %Y%m%d
        """
        return target.strftime('%Y%m%d')

    @staticmethod
    def today_str():
        """
        오늘 날짜
        :return: %Y-%m-%d
        """
        return datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def yesterday_str():
        """
        어제 날짜
        :return: %Y-%m-%d
        """
        old = datetime.now()
        added_date = old + relativedelta(days=-1)
        return added_date.strftime('%Y-%m-%d')

    @staticmethod
    def diff_days(date_str_1: str, date_str_2: str):
        """
        두 날짜 간의 차이 일 수
        :param date_str_1:
        :param date_str_2:
        :return:
        """
        date1 = datetime.strptime(date_str_1, '%Y-%m-%d')
        date2 = datetime.strptime(date_str_2, '%Y-%m-%d')
        return (date1 - date2).days

    @staticmethod
    def diff_min(date_1: datetime, date_2: datetime):
        """
        두 날짜 간의 차이 일 수
        :param date_1:
        :param date_2:
        :return:
        """
        return (date_1 - date_2).total_seconds() / 60

    @staticmethod
    def add_day(add_day: int):
        """
        날짜에 일 수 더하기
        :param add_day:
        :return: %Y-%m-%d
        """
        now = datetime.now()
        added_date = now + relativedelta(days=add_day)
        return added_date

    @staticmethod
    def add_day_str(old_day: str, add_day: int):
        """
        날짜에 일 수 더하기
        :param old_day:
        :param add_day:
        :return: %Y-%m-%d
        """
        old = datetime.strptime(old_day, '%Y-%m-%d')
        added_date = old + relativedelta(days=add_day)
        return added_date.strftime('%Y-%m-%d')

    @staticmethod
    def add_month_str(old_day: str = '', add_month: int = 0, add_day: int = 0):
        """
        날짜에 월 일 더하기
        :param old_day:
        :param add_month:
        :param add_day:
        :return: %Y-%m-%d
        """
        if old_day:
            today = datetime.strptime(old_day, '%Y-%m-%d')
        else:
            today = datetime.today()
        added_date = today + relativedelta(months=add_month)
        if add_day:
            added_date = added_date + relativedelta(days=add_day)
        return added_date.strftime('%Y-%m-%d')

    @staticmethod
    def add_minute_str(old_day: str = '', add_minute: int = 0):
        """
        날짜에 분 더하기
        :param old_day: %Y-%m-%d %H:%M:%S
        :param add_minute:
        :return: %Y-%m-%d %H:%M
        """
        if old_day:
            today = datetime.strptime(old_day, '%Y-%m-%d %H:%M:%S')
        else:
            today = datetime.today()
        added_date = today + relativedelta(minutes=add_minute)
        return added_date.strftime('%Y-%m-%d %H:%M')

    @staticmethod
    def make235959(target: date = ''):
        """
        23:59:59 만들기
        :param target: date
        :return: date 23:59:59
        """
        target_range = target + timedelta(days=1)
        return target_range - timedelta(microseconds=1)


    @staticmethod
    def generate235959(target: date = ''):
        """
        23:59:59 만들기
        :param target: date
        :return: date 23:59:59
        """
        date_time = datetime.now()
        date_time = date_time.replace(year=target.year, month=target.month, day=target.day, hour=23, minute=59, second=59)
        return date_time

    @staticmethod
    def str_convert(date_str: str):
        if date_str:
            if len(date_str) == 8:
                return datetime.strptime(date_str, "%Y%m%d")
            elif len(date_str) == 12:
                return datetime.strptime(date_str, "%Y%m%d%H%M")
            elif len(date_str) == 14:
                return datetime.strptime(date_str, "%Y%m%d%H%M%S")
            else:
                return None
        else:
            return None
