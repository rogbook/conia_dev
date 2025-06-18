from json import JSONDecodeError
import random

import requests
import bcrypt
from fastapi import APIRouter, Request, Depends, Form, status, Query
from fastapi.responses import RedirectResponse
from jose import jwt
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Customer, PaycoAuthCode, MemberStore, Store
from app.models.auth import MemberToken, AppleLogin
from app.models.customer import AddCustomer
from app.utils.jwt import token_user, token_user_option
from app.utils.common_utils import get_base_url
from app.routers.apis.auth import login_sns
from app.errors.exceptions import BadRequestEx, AlreadyDataEx, UnableStoreEx
from app.utils.log import analytics
from app.common.consts import AES_KEY, AES_IV, RANDOM_STRING_POOL
from app.utils.crypto_utils import AES256

router = APIRouter(prefix="/sns")


@router.get("/kakao-link")
def kakao_link(req: Request,
               session: Session = Depends(db.session),
               user: MemberToken = Depends(token_user)):
    res_token = requests.post(url="https://kauth.kakao.com/oauth/token", data={
        "grant_type": 'authorization_code',
        "client_id": '434945f5295e6a7f20a98cedb85e1b27',
        "redirect_uri": f'{get_base_url(req)}sns/kakao-link',
        "code": req.query_params.get('code')
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    token_data = res_token.json()

    if token_data.get('access_token'):
        res_user = requests.get("https://kapi.kakao.com/v1/user/access_token_info", headers={'Authorization': f'Bearer {token_data["access_token"]}'})
        user_data = res_user.json()

        already: Customer = Customer.filter(session, sns_kakao=user_data['id']).first()
        if already:
            already.sns_kakao = None

        customer = Customer.get(session, id=user.id)
        customer.sns_kakao = user_data['id']
        session.commit()

        store_code = req.cookies.get('current_store')
    else:
        raise BadRequestEx(reason='Code Error')

    return RedirectResponse(f'/{store_code}/member/profile')


@router.get("/kakao-login")
def kakao_login(req: Request,
                session: Session = Depends(db.session)):
    res_token = requests.post(url="https://kauth.kakao.com/oauth/token", data={
        "grant_type": 'authorization_code',
        "client_id": '434945f5295e6a7f20a98cedb85e1b27',
        "redirect_uri": f'{get_base_url(req)}sns/kakao-login',
        "code": req.query_params.get('code')
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    token_data = res_token.json()

    if token_data.get('access_token'):
        res_user = requests.get("https://kapi.kakao.com/v1/user/access_token_info", headers={'Authorization': f'Bearer {token_data["access_token"]}'})
        user_data = res_user.json()

        customer = Customer.get(session, sns_kakao=user_data['id'])
        store_code = req.cookies.get('current_store')

        response = RedirectResponse(f'/{store_code}')

        login_sns(response, customer, store_code, session)
    else:
        raise BadRequestEx(reason='Code Error')

    return response


@router.get("/google-link")
def google_link(req: Request,
                session: Session = Depends(db.session),
                user: MemberToken = Depends(token_user)):
    res_token = requests.post(url="https://oauth2.googleapis.com/token", data={
        "grant_type": 'authorization_code',
        "client_id": '288584913604-mee7d27m8u7gfdnropnnjb4m7g5qeneg.apps.googleusercontent.com',
        "client_secret": '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',
        "redirect_uri": f'{get_base_url(req)}sns/google-link',
        "code": req.query_params.get('code')
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    token_data = res_token.json()

    if token_data.get('id_token'):
        id_token: str = token_data["id_token"]
        payload = jwt.get_unverified_claims(id_token)

        already: Customer = Customer.filter(session, sns_google=payload['sub']).first()
        if already:
            already.sns_google = None

        customer = Customer.get(session, id=user.id)
        customer.sns_google = payload['sub']
        session.commit()

        store_code = req.cookies.get('current_store')
    else:
        raise BadRequestEx(reason='Code Error')

    return RedirectResponse(f'/{store_code}/member/profile')


@router.get("/google-login")
def google_login(req: Request,
                 session: Session = Depends(db.session)):
    res_token = requests.post(url="https://oauth2.googleapis.com/token", data={
        "grant_type": 'authorization_code',
        "client_id": '288584913604-mee7d27m8u7gfdnropnnjb4m7g5qeneg.apps.googleusercontent.com',
        "client_secret": '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',
        "redirect_uri": f'{get_base_url(req)}sns/google-login',
        "code": req.query_params.get('code')
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    token_data = res_token.json()

    if token_data.get('id_token'):
        id_token: str = token_data["id_token"]
        payload = jwt.get_unverified_claims(id_token)

        customer = Customer.get(session, sns_google=payload['sub'])
        store_code = req.cookies.get('current_store')

        response = RedirectResponse(f'/{store_code}')

        login_sns(response, customer, store_code, session)
    else:
        raise BadRequestEx(reason='Code Error')

    return response


@router.get("/payco-link")
def payco_link(req: Request,
               session: Session = Depends(db.session),
               user: MemberToken = Depends(token_user)):
    res_token = requests.post(url="https://id.payco.com/oauth2.0/token", data={
        "grant_type": 'authorization_code',
        "client_id": '3RDLN3dsub2LDYkyn0q5_Zq',
        "client_secret": '4Ck99GRh40LUcA_kgi5LNnSK',
        "code": req.query_params.get('code')
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    token_data = res_token.json()

    if token_data.get('access_token'):
        res_user = requests.post("https://apis-payco.krp.toastoven.net/payco/friends/find_member_v2.json", headers={'client_id': '3RDLN3dsub2LDYkyn0q5_Zq', 'access_token': token_data["access_token"]})
        user_data = res_user.json()

        already: Customer = Customer.filter(session, sns_payco=user_data['data']['member']['idNo']).first()
        if already:
            already.sns_payco = None

        customer = Customer.get(session, id=user.id)
        customer.sns_payco = user_data['data']['member']['idNo']
        session.commit()

        store_code = req.cookies.get('current_store')
    else:
        raise BadRequestEx(reason='Code Error')

    return RedirectResponse(f'/{store_code}/member/profile')


@router.get("/payco-login")
def payco_login(req: Request,
                session: Session = Depends(db.session)):
    res_token = requests.post(url="https://id.payco.com/oauth2.0/token", data={
        "grant_type": 'authorization_code',
        "client_id": '3RDLN3dsub2LDYkyn0q5_Zq',
        "client_secret": '4Ck99GRh40LUcA_kgi5LNnSK',
        "code": req.query_params.get('code')
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        token_data = res_token.json()
    except:
        analytics_data = {
            "type": "check",
            "file": "app/routers/sns.py",
            "func": "payco_login",
            "data": res_token.text,
        }
        analytics("store-log", analytics_data)
        raise BadRequestEx(reason='페이코 로그인 실패')

    if token_data.get('access_token'):
        res_user = requests.post("https://apis-payco.krp.toastoven.net/payco/friends/find_member_v2.json", headers={'client_id': '3RDLN3dsub2LDYkyn0q5_Zq', 'access_token': token_data["access_token"]})
        user_data = res_user.json()

        customer = Customer.get(session, sns_payco=user_data['data']['member']['idNo'])

        store_code = req.cookies.get('current_store')

        response = RedirectResponse(f'/{store_code}')

        login_sns(response, customer, store_code, session)
    else:
        raise BadRequestEx(reason='Code Error')

    return response


@router.get("/payco-code-login")
def payco_code_login(req: Request,
                     session: Session = Depends(db.session)):
    res_token = requests.post(url="https://id.payco.com/oauth2.0/token", data={
        "grant_type": 'authorization_code',
        "client_id": '3RDLN3dsub2LDYkyn0q5_Zq',
        "client_secret": '4Ck99GRh40LUcA_kgi5LNnSK',
        "code": req.query_params.get('code')
    }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    try:
        print(res_token.text)
        token_data = res_token.json()
    except:
        analytics_data = {
            "type": "check",
            "file": "app/routers/sns.py",
            "func": "payco_code_login",
            "data": res_token.text,
        }
        analytics("store-log", analytics_data)
        raise BadRequestEx(reason='페이코 로그인 실패')

    if token_data.get('access_token'):
        res_user = requests.post("https://apis-payco.krp.toastoven.net/payco/friends/find_member_v2.json", headers={'client_id': '3RDLN3dsub2LDYkyn0q5_Zq', 'access_token': token_data["access_token"]})
        user_data = res_user.json()

        payco_user_id_no = user_data['data']['member']['idNo']
        user_email = user_data['data']['member']['email']
        user_name = user_data['data']['member']['name']
        user_contact = user_data['data']['member']['contactNumber']

        params = {
            'idNo': payco_user_id_no,
            'mrcCd': 'HCK2K8'
        }
        res_payco_code = requests.get('https://mealticket-api.payco.com/api/mealticket/external/employee/merchant.nhn', params=params)
        try:
            payco_code_data = res_payco_code.json()
        except JSONDecodeError as je:
            print(res_payco_code.text)
            print(je.args)
            raise BadRequestEx(reason='기업코드 확인 불가')
        try:
            user_company_code = payco_code_data['result']['companyCode']
        except:
            print(payco_code_data)
            analytics_data = {
                "type": "check",
                "file": "app/routers/sns.py",
                "func": "payco_code_login/company_code",
                "data": res_payco_code.text,
            }
            analytics("store-log", analytics_data)
            raise BadRequestEx(reason='이용할 수 없는 상점입니다.')

        store_code = req.cookies.get('current_store')
        # able_codes = session.query(PaycoAuthCode).filter(PaycoAuthCode.store_code == store_code).all()
        if not store_code:
            store_code = req.query_params.get('state')
        store = session.query(Store).filter(Store.code == store_code).first()

        able = False
        # for able_code in able_codes:
        #     if able_code.code == user_company_code:
        #         able = True
        #         break
        if store.verify_code == user_company_code[:4]:
            able = True

        if not user_email:
            raise BadRequestEx(reason='이메일 정보를 확인 할 수 없습니다.')

        response = RedirectResponse(f'/{store_code}')
        if able:
            customer = Customer.get(session, sns_payco=payco_user_id_no)

            if not customer:
                email_customer = Customer.get(session, email=user_email)

                if not email_customer:
                    if user_contact:
                        passwd = user_contact[-4:]
                    else:
                        passwd = ''.join(random.choice(RANDOM_STRING_POOL) for _ in range(6))
                    hash_pw = bcrypt.hashpw(passwd.encode('utf8'), bcrypt.gensalt()).decode('utf8')
                    if user_contact:
                        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(user_contact)
                    else:
                        enc_mobile = None
                    join_platform = 'M' if req.state.device == 'MOBILE' else 'PC'
                    indata = AddCustomer(email=user_email, password=hash_pw, name=user_name, mobile=enc_mobile, mailling='N', sms='N', referer='payco', referer_domain='payco', join_platform=join_platform, sns_payco=payco_user_id_no)
                    customer = Customer.create(session, auto_commit=True, **indata.dict())
                    customer_id = customer.id
                else:
                    email_customer.sns_payco = payco_user_id_no
                    customer_id = email_customer.id

                ms = MemberStore()
                ms.customer_id = customer_id
                ms.store_code = store_code
                ms.value = "PAYCO_CERT"
                ms.confirm = "Y"
                session.add(ms)
                session.commit()
            else:
                ms = session.query(MemberStore).filter(MemberStore.customer_id == customer.id, MemberStore.store_code == store_code).first()
                if not ms:
                    ms = MemberStore()
                    ms.customer_id = customer.id
                    ms.store_code = store_code
                    ms.value = "PAYCO_CERT"
                    ms.confirm = "Y"
                    session.add(ms)
                    session.commit()
                elif ms.confirm != 'N':
                    ms.confirm = 'Y'
                    session.commit()

            login_sns(response, customer, store_code, session)
        else:
            raise BadRequestEx(reason='이용할 수 없는 상점입니다.')
    else:
        raise BadRequestEx(reason='Code Error')

    return response


@router.get("/naver-link")
def naver_link(req: Request,
               session: Session = Depends(db.session),
               user: MemberToken = Depends(token_user)):
    res_token = requests.post(url="https://nid.naver.com/oauth2.0/token", data={
        "grant_type": 'authorization_code',
        "client_id": '7eMzZBgkGyGvPFLenIja',
        "client_secret": 'adzA_cn96B',
        "code": req.query_params.get('code'),
        "state": 'naver',
    })

    token_data = res_token.json()

    if token_data.get('access_token'):
        res_user = requests.post("https://openapi.naver.com/v1/nid/me", headers={'Authorization': f'Bearer {token_data["access_token"]}'})
        user_data = res_user.json()

        already: Customer = Customer.filter(session, sns_naver=user_data['response']['id']).first()
        if already:
            already.sns_naver = None

        customer = Customer.get(session, id=user.id)
        customer.sns_naver = user_data['response']['id']
        session.commit()

        store_code = req.cookies.get('current_store')
    else:
        raise BadRequestEx(reason='Code Error')

    return RedirectResponse(f'/{store_code}/member/profile')


@router.get("/naver-login")
def naver_login(req: Request,
                session: Session = Depends(db.session)):
    res_token = requests.post(url="https://nid.naver.com/oauth2.0/token", data={
        "grant_type": 'authorization_code',
        "client_id": '7eMzZBgkGyGvPFLenIja',
        "client_secret": 'adzA_cn96B',
        "code": req.query_params.get('code'),
        "state": 'naver',
    })

    token_data = res_token.json()

    if token_data.get('access_token'):
        res_user = requests.post("https://openapi.naver.com/v1/nid/me", headers={'Authorization': f'Bearer {token_data["access_token"]}'})
        user_data = res_user.json()

        customer = Customer.get(session, sns_naver=user_data['response']['id'])
        store_code = req.cookies.get('current_store')

        response = RedirectResponse(f'/{store_code}')

        login_sns(response, customer, store_code, session)
    else:
        raise BadRequestEx(reason='Code Error')

    return response


@router.post("/apple-link")
def apple_link(req: Request,
               id_token: str = Form(),
               state: str = Form(),
               session: Session = Depends(db.session)):
    payload = jwt.get_unverified_claims(id_token)

    already: Customer = Customer.filter(session, sns_apple=payload['sub']).first()
    if already:
        already.sns_apple = None

    data = state.split('_')
    customer = Customer.get(session, id=state[0])
    customer.sns_apple = payload['sub']
    session.commit()

    store_code = data[1]

    return RedirectResponse(f'/{store_code}/member/profile', status_code=status.HTTP_302_FOUND)


@router.post("/apple-login")
def apple_login(req: Request,
                id_token: str = Form(),
                state: str = Form(),
                session: Session = Depends(db.session)):
    payload = jwt.get_unverified_claims(id_token)

    customer = Customer.get(session, sns_apple=payload['sub'])
    store_code = state

    response = RedirectResponse(f'/{store_code}', status_code=status.HTTP_302_FOUND)

    login_sns(response, customer, store_code, session)

    return response


@router.get("/apple")
def apple(req: Request,
          call_type: str = Query(),
          id_token: str = Query(),
          store_code: str = Query(),
          session: Session = Depends(db.session),
          user: MemberToken = Depends(token_user_option)):
    payload = jwt.get_unverified_claims(id_token)

    if call_type == "link":
        already: Customer = Customer.filter(session, sns_apple=payload['sub']).first()
        if already:
            already.sns_apple = None

        customer = Customer.get(session, id=user.id)
        customer.sns_apple = payload['sub']
        session.commit()
        response = RedirectResponse(f'/{store_code}/member/profile')
    else:
        customer = Customer.get(session, sns_apple=payload['sub'])
        response = RedirectResponse(f'/{store_code}')
        login_sns(response, customer, store_code, session)

    return response
