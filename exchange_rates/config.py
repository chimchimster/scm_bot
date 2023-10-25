from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigAPI(BaseSettings):
    api_key: SecretStr
    api_url: SecretStr
    model_config = SettingsConfigDict(env_file=Path.cwd() / '.env', env_file_encoding='utf-8')


config_api = ConfigAPI()