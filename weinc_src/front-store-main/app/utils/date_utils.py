from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time


class D:
    """
    날짜,시간 관련 유틸
    """
    def __init__(self):
        self.utc_now = datetime.utcnow()
        self.now = datetime.now()
        self.time = time.time()

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
    def convert_yyyymmdd(date: datetime):
        """
        시간 변환
        :return: %Y%m%d
        """
        return date.strftime('%Y%m%d')

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
    def tomorrow_str():
        """
        내일 날짜
        :return: %Y-%m-%d
        """
        old = datetime.now()
        added_date = old + relativedelta(days=1)
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
    def add_day_zero_hour(add_day: int):
        """
        날짜에 일 수 더한 후 0시로 설정
        :param add_day:
        :return: %Y-%m-%d
        """
        now = datetime.now()
        added_date = now + relativedelta(days=add_day)
        added_date = added_date.replace(hour=0, minute=0, second=0, microsecond=0)
        return added_date

    @staticmethod
    def add_day_last_hour(add_day: int):
        """
        날짜에 일 수 더한 후 23시 59분 59초로 설정
        :param add_day:
        :return: %Y-%m-%d
        """
        now = datetime.now()
        added_date = now + relativedelta(days=add_day)
        added_date = added_date.replace(hour=23, minute=59, second=59, microsecond=0)
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
    def between_date(start_date: str, end_date: str):
        """
        현재 시간이 시작 시간과 종료 시간 사이에 있는지 판별
        :param start_date:
        :param end_date:
        :return:
        """
        start = None
        end = None

        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        now = datetime.now()

        if start and end:
            return start <= now <= end
        elif start:
            return start <= now
        elif end:
            return now <= end

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

    @staticmethod
    def set_day(day: int):
        if day:
            now = datetime.now()
            return now.replace(day=day, hour=0, minute=0, second=0, microsecond=0)
        else:
            return None

    @staticmethod
    def set_week(week: int):
        now = datetime.now()
        if week == 0:
            target_week = 6
        else:
            target_week = week - 1
        days_until_target = target_week - now.weekday()
        target_date = now + timedelta(days=days_until_target)

        return target_date.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_last_week(week: int):
        now = datetime.now()
        if week == 0:
            target_week = 6
        else:
            target_week = week - 1

        days_until_target = (now.weekday() - target_week) % 7
        target_date = now - timedelta(days=days_until_target)

        return target_date.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_last_day(day: int):
        if day:
            now = datetime.now()
            year = now.year
            month = now.month

            if now.day < day:
                # 이전 달로 이동
                if month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1

            try:
                target_date = datetime(year, month, day)
            except ValueError:
                # 이전 달에 day가 없으면 마지막 날로 설정
                last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day
                target_date = datetime(year, month, last_day)

            return target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            return None
