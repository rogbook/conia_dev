import requests
import hashlib
import hmac
import time
import json
from base64 import b64encode
from app.utils.date_utils import D
from app.common.consts import NICE_TOKEN, NICE_CLIENT_ID, NICE_CLIENT_SECRET, NICE_PRODUCT_ID
from app.utils.crypto_utils import AES128


NICE_HOST = 'https://svc.niceapi.co.kr:22001'


def get_api_token():
    """
    API 서비스 이용 토큰 발급
    :return:
    """
    auth = f'{NICE_CLIENT_ID}:{NICE_CLIENT_SECRET}'
    auth_enc = b64encode(auth.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_enc}'
    }
    post_data = {
        'grant_type': 'client_credentials',
        'scope': 'default'
    }
    res = requests.post(f'{NICE_HOST}/digital/niceid/oauth/oauth/token', headers=headers, data=post_data)
    result = res.json()
    data = None
    if result['dataHeader']['GW_RSLT_CD'] == '1200':
        data = {
            'access_token': result['dataBody']['access_token'],
            'token_type': result['dataBody']['token_type'],
            'expires_in': result['dataBody']['expires_in'],
            'scope': result['dataBody']['scope']
        }
    return data


def revoke_api_token():
    """
    API 서비스 이용 토큰 폐기
    :return: 처리 결과
    """
    time_stamp = int(time.time())
    auth = f'{NICE_TOKEN}:{time_stamp}:{NICE_CLIENT_ID}'
    auth_enc = b64encode(auth.encode('utf-8')).decode('utf-8')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_enc}'
    }

    res = requests.post(f'{NICE_HOST}/digital/niceid/oauth/oauth/token', headers=headers)
    result = res.json()
    if result['dataHeader']['GW_RSLT_CD'] == '1200':
        return True
    return False


def get_token():
    time_stamp = int(time.time())
    auth = f'{NICE_TOKEN}:{time_stamp}:{NICE_CLIENT_ID}'
    auth_enc = b64encode(auth.encode('utf-8')).decode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'bearer {auth_enc}',
        'ProductID': NICE_PRODUCT_ID,
    }
    req_dtim = D().now_str_trim()
    req_no = str(int(D().milli_time()))
    pay_load = {
        'dataHeader': {
            'CNTY_CD': 'ko'
        },
        'dataBody': {
            'req_dtim': req_dtim,
            'req_no': req_no,
            'enc_mode': '1',
        }
    }
    res = requests.post(f'{NICE_HOST}/digital/niceid/api/v1.0/common/crypto/token',
                        headers=headers, json=pay_load)
    result = res.json()
    data = None
    if result['dataHeader']['GW_RSLT_CD'] == '1200':
        if result['dataBody']['rsp_cd'] == 'P000':
            if result['dataBody']['result_cd'] == '0000':
                data = {
                    'req_dtim': req_dtim,
                    'req_no': req_no,
                    'site_code': result['dataBody']['site_code'],
                    'token_version_id': result['dataBody']['token_version_id'],
                    'token_val': result['dataBody']['token_val']
                }
    return data


def make_key(data):
    in_data = f"{data['req_dtim']}{data['req_no']}{data['token_val']}"
    sha = hashlib.sha256(in_data.encode()).digest()
    b64_str = b64encode(sha)
    key = b64_str[:16]
    iv = b64_str[-16:]
    hmac_key = b64_str[:32]

    return key, iv, hmac_key


def enc_req_data(receive_data, return_url):
    data = get_token()
    key, iv, hmac_key = make_key(data)

    cipher = AES128(key, iv)

    enc_raw = {
        "requestno": f"REQ{data['req_no']}",
        "returnurl": return_url,
        "sitecode": data['site_code'],
        "methodtype": "get",
        "popupyn": "Y",
        "receivedata": receive_data if receive_data else ""
    }
    enc = cipher.encrypt(json.dumps(enc_raw))

    hmac_str = hmac.new(hmac_key, msg=enc.encode(), digestmod=hashlib.sha256).digest()
    integrity_value = b64encode(hmac_str).decode('utf-8')

    res = {
        'key': key.decode(),
        'iv': iv.decode(),
        'token_version_id': data['token_version_id'],
        'enc_data': enc,
        'integrity_value': integrity_value
    }

    return res


def dec_res_data(key, iv, enc_data):
    aes = AES128(key.encode(), iv.encode())
    dec_data = aes.decrypt(enc_data, 'euc-kr')
    return dec_data
