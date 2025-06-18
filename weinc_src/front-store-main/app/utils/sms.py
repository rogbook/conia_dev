import requests
from app.common.consts import CONIA_SMS_URL, CONIA_SMS_TOKEN, CONIA_SMS_SENDER


class SMS:
    def __init__(self):
        self.url = CONIA_SMS_URL
        self.token = CONIA_SMS_TOKEN

    def send(self, receiver, msg, title=None, r_datetime=None):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'bearer {self.token}',
        }
        pay_load = dict(
            sender=CONIA_SMS_SENDER,
            receiver=receiver,
            msg=msg
        )
        if title:
            pay_load.update(title=title)
        if r_datetime:
            pay_load.update(r_datetime=r_datetime)

        res = requests.post(f'{CONIA_SMS_URL}/sms/send', headers=headers, json=pay_load)

        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Error')

    def cancel(self, mid):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'bearer {self.token}',
        }
        pay_load = dict(
            mid=mid
        )

        res = requests.post(f'{CONIA_SMS_URL}/sms/cancel', headers=headers, json=pay_load)

        if res.status_code == 200:
            return res.json()
        else:
            raise Exception('Error')
