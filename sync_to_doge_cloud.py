import boto3
import os
from pathlib import Path
from botocore.client import Config

# 从环境变量中获取配置
BUCKET_NAME = os.getenv('COS_BUCKET')
ENDPOINT = os.getenv('COS_ENDPOINT')
ACCESS_KEY = os.getenv('COS_SECRET_ID')
SECRET_KEY = os.getenv('COS_SECRET_KEY')

# 打印调试信息
print("BUCKET_NAME:", BUCKET_NAME)
print("ENDPOINT:", ENDPOINT)
print("ACCESS_KEY:", ACCESS_KEY)
print("SECRET_KEY:", SECRET_KEY)

# 创建 COS 客户端，指定虚拟主机样式访问
s3_client = boto3.client(
    's3',
    endpoint_url=ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(s3={'addressing_style': 'virtual'})
)

# 上传目录中的文件到多吉云
def upload_to_cos(directory, bucket_name):
    for file_path in Path(directory).rglob('*'):
        if file_path.is_file():
            with open(file_path, 'rb') as data:
                s3_client.upload_fileobj(data, bucket_name, str(file_path.relative_to(directory)))

# 上传整个仓库内容
upload_to_cos('.', BUCKET_NAME)
