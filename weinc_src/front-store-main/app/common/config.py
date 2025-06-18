from dataclasses import dataclass
from os import path, environ


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    """
    기본 설정 값
    """
    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = False
    DB_URL: str = environ.get("DB_URL", "mysql+pymysql://user@host/conia?charset=utf8mb4")
    MONGO_DB_URL: str = environ.get("MONGO_DB_URL", "mongodb://conia:Ac2022!!@aconic-gidc.iptime.org")
    REDIS_URL: str = environ.get("REDIS_URL", "redis://aconic-gidc.iptime.org:6379")
    API_HOST = "https://v3api.coniaworld.com"
    DEBUG: bool = True
    TEST_MODE: bool = False
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    PG_KCP_HOST = "https://stg-spl.kcp.co.kr"
    PG_KCP_PC_HOST = "https://testspay.kcp.co.kr/plugin/kcp_spay_hub.js"
    PG_KCP_SITE_CODE = "T0000"
    PG_KCP_CERT_INFO = "-----BEGIN CERTIFICATE-----MIIDgTCCAmmgAwIBAgIHBy4lYNG7ojANBgkqhkiG9w0BAQsFADBzMQswCQYDVQQGEwJLUjEOMAwGA1UECAwFU2VvdWwxEDAOBgNVBAcMB0d1cm8tZ3UxFTATBgNVBAoMDE5ITktDUCBDb3JwLjETMBEGA1UECwwKSVQgQ2VudGVyLjEWMBQGA1UEAwwNc3BsLmtjcC5jby5rcjAeFw0yMTA2MjkwMDM0MzdaFw0yNjA2MjgwMDM0MzdaMHAxCzAJBgNVBAYTAktSMQ4wDAYDVQQIDAVTZW91bDEQMA4GA1UEBwwHR3Vyby1ndTERMA8GA1UECgwITG9jYWxXZWIxETAPBgNVBAsMCERFVlBHV0VCMRkwFwYDVQQDDBAyMDIxMDYyOTEwMDAwMDI0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAppkVQkU4SwNTYbIUaNDVhu2w1uvG4qip0U7h9n90cLfKymIRKDiebLhLIVFctuhTmgY7tkE7yQTNkD+jXHYufQ/qj06ukwf1BtqUVru9mqa7ysU298B6l9v0Fv8h3ztTYvfHEBmpB6AoZDBChMEua7Or/L3C2vYtU/6lWLjBT1xwXVLvNN/7XpQokuWq0rnjSRThcXrDpWMbqYYUt/CL7YHosfBazAXLoN5JvTd1O9C3FPxLxwcIAI9H8SbWIQKhap7JeA/IUP1Vk4K/o3Yiytl6Aqh3U1egHfEdWNqwpaiHPuM/jsDkVzuS9FV4RCdcBEsRPnAWHz10w8CX7e7zdwIDAQABox0wGzAOBgNVHQ8BAf8EBAMCB4AwCQYDVR0TBAIwADANBgkqhkiG9w0BAQsFAAOCAQEAg9lYy+dM/8Dnz4COc+XIjEwr4FeC9ExnWaaxH6GlWjJbB94O2L26arrjT2hGl9jUzwd+BdvTGdNCpEjOz3KEq8yJhcu5mFxMskLnHNo1lg5qtydIID6eSgew3vm6d7b3O6pYd+NHdHQsuMw5S5z1m+0TbBQkb6A9RKE1md5/Yw+NymDy+c4NaKsbxepw+HtSOnma/R7TErQ/8qVioIthEpwbqyjgIoGzgOdEFsF9mfkt/5k6rR0WX8xzcro5XSB3T+oecMS54j0+nHyoS96/llRLqFDBUfWn5Cay7pJNWXCnw4jIiBsTBa3q95RVRyMEcDgPwugMXPXGBwNoMOOpuQ==-----END CERTIFICATE-----"
    PG_KCP_CERT_FILE = "splPrikeyPKCS8.pem"
    PG_KCP_CERT_PASSWD = "changeit"
    PG_PAYCO_HOST = "https://alpha-api-bill.payco.com"
    PG_PAYCO_SELLER_KEY = "S0FSJE"
    PG_PAYCO_CP_ID = "PARTNERTEST"
    PG_PAYCO_PRODUCT_ID = "PROD_EASY"

    ECOUPON_M12_HOST = "https://sdev.giftpop.co.kr:10901"
    ECOUPON_M12_SID = "SAMPLE01"
    ECOUPON_M12_KEY = "ROCOMO02M12GRD4Y"
    ECOUPON_M12_IV = "M12ROCOMO33FEW4T"

    ECOUPON_DNC_HOST = "https://partners-stage.bizpopcon.com"
    ECOUPON_DNC_KEY = "90e45efde4c29fdc0183f6222b7cc4a481ef248eb5b534fa200576307a4b64ef"
    ECOUPON_DNC_CAMPAIGN_CODE = "M2413001"

    ECOUPON_KT_HOST = "http://tgiftishowgw.giftishow.co.kr"
    ECOUPON_KT_KEY = "DVI5M7SBWG5SASJVM9MCYJVK9N7QB5L2"
    ECOUPON_KT_AUTH_CODE = "M000218081"
    ECOUPON_KT_AUTH_TOKEN = "ybywoswjPhqeONZnMQJzXA=="
    ECOUPON_KT_TEMPLATE_CODE = "202412160008749"


@dataclass
class LocalConfig(Config):
    DB_URL: str = environ.get("DB_URL", "sqlite:///./test.db")
    MONGO_DB_URL: str = environ.get("MONGO_DB_URL", "mongodb://conia:Ac2022!!@aconic-gidc.iptime.org")


@dataclass
class ProdConfig(Config):
    DB_URL: str = environ.get("DB_URL", "mysql+pymysql://conia_store:2AWEXM1Eg1orqFL@database-coniaworld.cuxhbcfwbgw4.ap-northeast-2.rds.amazonaws.com:3107/conia?charset=utf8mb4")
    MONGO_DB_URL: str = environ.get("MONGO_DB_URL", "mongodb://conia:Uf5yDhlflR3E5rv@ec2-3-35-223-209.ap-northeast-2.compute.amazonaws.com:21028")
    REDIS_URL: str = environ.get("REDIS_URL", "redis://ec2-3-35-223-209.ap-northeast-2.compute.amazonaws.com:6379")
    API_HOST = "https://api.coniaworld.com"
    TRUSTED_HOSTS = ["*.coniaworld.com"]
    ALLOW_SITE = ["*.coniaworld.com"]
    DEBUG: bool = False
    PG_KCP_HOST = "https://spl.kcp.co.kr"
    PG_KCP_PC_HOST = "https://spay.kcp.co.kr/plugin/kcp_spay_hub.js"
    PG_KCP_SITE_CODE = "AIZJA"
    PG_KCP_CERT_INFO = "-----BEGIN CERTIFICATE-----MIIDjDCCAnSgAwIBAgIHBy/vxnG50DANBgkqhkiG9w0BAQsFADBzMQswCQYDVQQGEwJLUjEOMAwGA1UECAwFU2VvdWwxEDAOBgNVBAcMB0d1cm8tZ3UxFTATBgNVBAoMDE5ITktDUCBDb3JwLjETMBEGA1UECwwKSVQgQ2VudGVyLjEWMBQGA1UEAwwNc3BsLmtjcC5jby5rcjAeFw0yMzAzMTcwNzA0MjhaFw0yODAzMTUwNzA0MjhaMHsxCzAJBgNVBAYTAktSMQ4wDAYDVQQIDAVTZW91bDEQMA4GA1UEBwwHR3Vyby1ndTEWMBQGA1UECgwNTkhOIEtDUCBDb3JwLjEXMBUGA1UECwwOUEdXRUJERVYgVGVhbS4xGTAXBgNVBAMMEDIwMjMwMzE3MTAwMDQ5MDcwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCk/wY/FS0KCe5tVgsv7OU8R9DILTVgXoaWQNL6PZhJmq+mNsdZ8lfJ5K2agFP9P3v7XVJsHix1sDsy2FXTgABqBTMuP0N+7C9o0cL2JvsiZIXDIfnGHHD+U40LrsNgsRF57MxWsXySo37wUqmaemUjKYKnwTaXRHB6aeicwJaA13QSjUT7BTs0F/LG2kqhK1TYyYY1scyEm2JklJyh3SKLeIJnDlBxSsrpE7AmvDilqJlB58mfxdVJ42GcOL+/YdJXhnPrVZhITvDjaX6cnhej5nFpZ/u/OUsfqc7og/3l/eRaNbZkSCOfrmQ/yR6BBD6ETYMmNK/Ch6GcWc6bJ6g/AgMBAAGjHTAbMA4GA1UdDwEB/wQEAwIHgDAJBgNVHRMEAjAAMA0GCSqGSIb3DQEBCwUAA4IBAQC55aTWHiKpQVJT9gnXQ5Yn/m0yh2OORwZEJQHe0nqQfy1uhuB+Dh6XkxgF8k9E/xF/tbjdJ2egPpg2zSTeSMdGutCifPWOT+//kzlsi8Cm8X7gsVmOeKiuTD7jlIlznQ2JgpHnlYHw25t46T7aGPg9W6QUJEiNyTYTRV3zqBuMfQy4JG+slYTMrGR5btarEIYwUYhMXp1lkEcWF0ZD0sU+Qz5hpGWhp9UvS3doEWEYi0HHv2ms0908ki3lDMRC8rU+k9xIU2Z8fgN4V1D/WNgtfF9wns14qWRd41/UYdSPKdXjlYu0vdu4KAVSK6M6YmdJhaBNyvu/RXylLyKlQ+Kx-----END CERTIFICATE-----"
    PG_KCP_CERT_FILE = "KCP_AUTH_AIZJA_PRIKEY.pem"
    PG_KCP_CERT_PASSWD = "7Pu37PT7@bMMs*8@"
    PG_PAYCO_HOST = "https://api-bill.payco.com"
    PG_PAYCO_SELLER_KEY = "1XUMIR"
    PG_PAYCO_CP_ID = "1XUMIR"
    PG_PAYCO_PRODUCT_ID = "1XUMIR_EASYP"

    ECOUPON_M12_HOST = "https://smc23.giftpop.co.kr:10901"
    ECOUPON_M12_SID = "CONIALAB"
    ECOUPON_M12_KEY = "EGN4LKBXR0UEPDYU"
    ECOUPON_M12_IV = "T9ZNG45AEO6NWN74"

    ECOUPON_DNC_HOST = ""
    ECOUPON_DNC_KEY = ""
    ECOUPON_DNC_CAMPAIGN_CODE = ""

    ECOUPON_KT_HOST = "https://giftishowgw.giftishow.co.kr"
    ECOUPON_KT_KEY = "DVI5M8RIWG6T6VD2J8UEZBYJ4U8RF2OA"
    ECOUPON_KT_AUTH_CODE = "M000156749"
    ECOUPON_KT_AUTH_TOKEN = "zNFg/x8VzMiFcO7dKur8uw=="
    ECOUPON_KT_TEMPLATE_CODE = "202412170279207"


@dataclass
class TestConfig(Config):
    DB_URL: str = environ.get("DB_URL", "mysql+pymysql://conia:Ac2022!!@test.coniaworld.com/conia?charset=utf8mb4")
    MONGO_DB_URL: str = environ.get("MONGO_DB_URL", "mongodb://conia:Ac2022!!@test.coniaworld.com")
    REDIS_URL: str = environ.get("REDIS_URL", "redis://aconic-gidc.iptime.org:6379")
    TEST_MODE: bool = True


def conf() -> Config:
    """
    환경 불러오기
    :return: Config
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("CONFIG_ENV", "local")]()
