from ..core.database import S3Data
from ..thirdparty.S3.s3 import s3


def s3_job(bucket):
    DB = S3Data(bucket)
    total = s3(bucket).result
    DB.insert_bucket(total)
    return total

def get_s3(bucket):
    DB = S3Data(bucket)
    return DB.read_bucket()