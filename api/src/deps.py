from functools import cache
from typing import Annotated

import aioboto3
import catboost
from fastapi import Depends

from prediction import Predictor
from settings import Settings, create_settings

Config = Annotated[Settings, Depends(create_settings)]


@cache
def cached_predictor(model_path: str) -> Predictor:
    predictor = Predictor(
        catboost.CatBoostClassifier().load_model(model_path)
    )
    return predictor


def create_predictor(config: Config) -> Predictor:
    return cached_predictor(config.MODEL_PATH)


async def create_s3_client(config: Config):
    session = aioboto3.Session()
    client = session.client(
        's3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=config.S3_ACCESS_KEY_ID,
        aws_secret_access_key=config.S3_SECRET_ACCESS_KEY,
    )
    async with client as s3:
        yield s3


PredictorInstance = Annotated[Predictor, Depends(create_predictor)]
S3Client = Annotated[aioboto3.Session, Depends(create_s3_client)]
