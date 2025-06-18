import time

from sqlalchemy.orm import Session
import openpyxl
import bcrypt
import pyotp

from app.common.consts import AES_KEY, AES_IV
from app.utils.crypto_utils import AES256
from app.utils.aws import SES
from app.common.template_string import PASSWD_RESET

from app.database.schema import Class, Permission, Member
from scripts.database.conn import db


if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        target_list = [('', '')]
        ses = SES()

        for target in target_list:
            email_body = PASSWD_RESET.format(name=target[1], email=target[0])
            ses.send_email(target[0], '[윙크] 새로운 시작을 위한 비밀번호 업데이트 완료', email_body)


    db.shutdown()
