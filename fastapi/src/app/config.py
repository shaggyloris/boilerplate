import os
import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Contains relevant settings for the application.
    
    Data can be parsed from secrets, environment variables, or an environment file
    """
    app_name: str = "my-api"

    # For authentication
    secret_key: str = hex(secrets.randbits(256))
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    
    class Config:
        env_file = "/data/.env"
        env_file_encoding = "utf-8"
        # If this doesn't exist, you will get a warning
        secrets_dir = "/run/secrets"


# Allow the .env file path to (optionally) be specified as an environment variable itself. This helps with testing
env_file_path = os.getenv("ENV_FILE_PATH")
# Instantiate the settings object that is used in the application
if env_file_path:
    settings = Settings(_env_file_path=env_file_path)
else:
    settings = Settings()
