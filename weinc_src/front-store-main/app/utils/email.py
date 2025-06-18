import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_SERVER = "smtp.mailplug.co.kr"
MAIL_PORT = 465
MAIL_SENDER_USERNAME = "noreply@conia.co.kr"
MAIL_SENDER_PASSWORD = "hodumaru2!"
MAIL_USE_TLS = False
MAIL_USE_SSL = True


class SendEmail:
    def __init__(self):
        self.smtp = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        self.smtp.login(MAIL_SENDER_USERNAME, MAIL_SENDER_PASSWORD)

    def send(self, to, subject, body):
        message = MIMEMultipart()
        message['From'] = MAIL_SENDER_USERNAME
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(body, _subtype='html'))

        self.smtp.send_message(message)
        self.smtp.quit()