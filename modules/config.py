import yaml
from pydantic import BaseModel

CONFIG_FILE_PATH = "config.yml"  # with respect to directory of project


class MeiliSearchConfig(BaseModel):
    host: str
    port: int
    db_path: str
    index_name: str
    index_primary_key: str
    startup_args: list[str]


class DatabaseConfig(BaseModel):
    meilisearch: MeiliSearchConfig


class AudioConfig(BaseModel):
    scan_directories: list[str]
    scan_formats: list[str]


class Config(BaseModel):
    database: DatabaseConfig
    audio: AudioConfig

    @classmethod
    def get_base_configuration(cls) -> "Config":
        with open(CONFIG_FILE_PATH, "r") as file:
            config_data = yaml.safe_load(file)
        return cls(**config_data)
