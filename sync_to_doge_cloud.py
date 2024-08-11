import boto3
import os
from pathlib import Path

# 从环境变量中获取配置
BUCKET_NAME = os.getenv('COS_BUCKET')
ENDPOINT = os.getenv('COS_ENDPOINT')
ACCESS_KEY = os.getenv('COS_SECRET_ID')
SECRET_KEY = os.getenv('COS_SECRET_KEY')

# 创建 COS 客户端
s3_client = boto3.client(
    's3',
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# 上传目录中的文件到多吉云
def upload_to_cos(directory, bucket_name):
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            with open(file_path, 'rb') as data:
                s3_client.upload_fileobj(data, bucket_name, str(file_path.relative_to(directory)))

# 上传整个仓库内容
upload_to_cos('.', BUCKET_NAME)
