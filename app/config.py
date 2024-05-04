from pydantic import BaseSettings

# Pydantic can help us to retrieve and validate environment variables set on our system.
# Via the BaseSettings class, we can create a Settings object whose attributes are case-insensitive
# references to environment variables. We can also assign them default values.
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # we can also tell pydantic to import environment variables from an '.env' file and not from the system
    class Config:
        env_file = "./.env"

# instantiate our Settings object
settings = Settings()