import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosServiceError

# 从环境变量中获取配置信息
secret_id = os.getenv('COS_SECRET_ID')
secret_key = os.getenv('COS_SECRET_KEY')
region = os.getenv('COS_REGION')
bucket = os.getenv('COS_BUCKET')
endpoint = os.getenv('COS_ENDPOINT')

# 初始化 COS 配置和客户端
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Endpoint=endpoint)
client = CosS3Client(config)

def upload_file(local_path, cos_key):
    """上传单个文件到 COS"""
    try:
        response = client.upload_file(
            Bucket=bucket,
            LocalFilePath=local_path,
            Key=cos_key,
        )
        print(f"Uploaded {local_path} to {cos_key}: {response['ETag']}")
    except CosServiceError as e:
        print(f"Failed to upload {local_path}: {e}")

def upload_directory(directory, prefix=''):
    """递归上传目录下的所有文件到 COS"""
    for root, _, files in os.walk(directory):
        for file in files:
            local_path = os.path.join(root, file)
            cos_key = os.path.join(prefix, os.path.relpath(local_path, directory)).replace("\\", "/")
            upload_file(local_path, cos_key)

# 开始上传整个项目目录
upload_directory('.')
