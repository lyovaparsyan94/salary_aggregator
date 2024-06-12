import os
from os.path import join

from pydantic_settings import BaseSettings

BASE_DIR = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(BASE_DIR))
ENV_DIR = join(project_dir, '.env')


class PrivateConfigs(BaseSettings):
    TELEGRAM_TOKEN: str
    MONGO_URI: str

    class Config:
        env_file = ENV_DIR
        extra = "allow"


class DirConfigs(BaseSettings):
    ROOT_DIR: str = os.path.dirname(os.path.dirname(BASE_DIR))
    SRC_DIR: str = os.path.dirname(BASE_DIR)
    DATA_DIR: str = join(SRC_DIR, join('data'))
    BSON_COLLECTION_DIR: str = join(DATA_DIR, join('sample_collection.bson'))
    COLLECTION_METADATA_DIR: str = join(DATA_DIR, join('sample_collection.metadata.json'))


class Config(BaseSettings):
    PRIVATE_CONFIGS: PrivateConfigs = PrivateConfigs()
    DIR_CONFIG: DirConfigs = DirConfigs()


configs = Config()
