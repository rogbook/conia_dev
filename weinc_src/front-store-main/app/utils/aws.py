import boto3
from botocore.exceptions import ClientError

from app.common.consts import AWS_ACCESS_KEY, AWS_ACCESS_SECRET, AWS_REGION


class S3:

    def __init__(self):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=AWS_ACCESS_KEY,
                               aws_secret_access_key=AWS_ACCESS_SECRET,
                               region_name=AWS_REGION)

    def upload_file(self, file, bucket, folder_name, file_name):
        return self.s3.upload_fileobj(file.file, bucket, f"{folder_name}{file_name}", ExtraArgs={"ContentType": file.content_type})


class SES:
    def __init__(self):
        self.ses = boto3.client('ses',
                                region_name=AWS_REGION,
                                aws_access_key_id=AWS_ACCESS_KEY,
                                aws_secret_access_key=AWS_ACCESS_SECRET)

    def send_email(self, to, subject, message):
        try:
            # Provide the contents of the email.
            response = self.ses.send_email(
                Destination={
                    'ToAddresses': [to]
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': 'UTF-8',
                            'Data': message,
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
                },
                Source='noreply@conia.co.kr',
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])