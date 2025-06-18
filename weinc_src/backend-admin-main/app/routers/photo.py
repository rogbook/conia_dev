from uuid import uuid4

from fastapi import APIRouter, Depends, Security, UploadFile, Request, Query

from app.common.consts import AWS_S3_BUCKET_IMG, AWS_S3_BUCKET_IMG_HOST
from app.models.auth import MemberToken
from app.models.common import CreatedURI
from app.utils.aws import S3
from app.utils.common_utils import extensions, get_ip
from app.utils.date_utils import D
from app.utils.jwt import token_user
from app.utils.log import data_logger

router = APIRouter(prefix='/photo')


@router.post("", response_model=CreatedURI, name="이미지 등록")
def add_photo(req: Request,
              file: UploadFile,
              path: str = Query(description="경로"),
              ext: str = Depends(extensions),
              user: MemberToken = Security(token_user, scopes=[])):
    """
    경로 값 예시 '경로1/' 또는 경로2/경로3/
    """
    s3 = S3()

    file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{ext}"
    s3.upload_file(file, AWS_S3_BUCKET_IMG, path, file_name)
    url: str = f"{AWS_S3_BUCKET_IMG_HOST}{path}{file_name}"

    log_dict = dict(
        category=path,
        action="add file",
        type="image",
        ip=get_ip(req),
        user=user.id,
        user_name=user.name,
        data=url,
    )
    data_logger(log_dict)

    return CreatedURI(uri=url)
