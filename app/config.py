from pydantic import BaseModel
from typing import List
import yaml

CONFIG_FILE_PATH = "config.yml"  # with respect to directory of project


class DatabaseConfig(BaseModel):
    host: str
    port: int


class AudioConfig(BaseModel):
    scan_directories: List[str]


class Config(BaseModel):
    database: DatabaseConfig
    audio: AudioConfig


class _ConfigLoader:
    _config: Config

    @classmethod
    def load_config(cls, config_file=CONFIG_FILE_PATH):
        with open(config_file, "r") as file:
            config_data = yaml.safe_load(file)
        cls._config = Config(**config_data)
        return cls._config

    @classmethod
    def get_config(cls) -> Config:
        if not hasattr(cls, "_config"):
            cls.load_config()
        return cls._config


# Initialize the configuration during startup, this should be imported throughout the project. This is inherently singleton
config = _ConfigLoader.get_config()
