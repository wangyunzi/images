import boto3
from botocore.client import Config
from pathlib import Path

# 配置信息
BUCKET_NAME = 's-sh-4319-blog-1258813047'
ENDPOINT = 'https://cos.ap-shanghai.myqcloud.com'
ACCESS_KEY = 'c1c06722b68f3327'
SECRET_KEY = '799e18e52933b9e71fbc4261a139a51d'

# 创建 COS 客户端
s3_client = boto3.client(
    's3',
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(s3={'addressing_style': 'virtual'})
)

# 上传文件函数
def upload_to_cos(directory, bucket_name):
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            with open(file_path, 'rb') as data:
                s3_client.upload_fileobj(data, bucket_name, str(file_path.relative_to(directory)))
                print(f"Uploaded: {file_path}")

# 执行上传
upload_to_cos('.', BUCKET_NAME)
