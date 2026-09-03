from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mysql_url: str = "mysql+pymysql://treecare:treecarepw@127.0.0.1:3307/treecare"

    snowflake_account: str | None = None
    snowflake_user: str | None = None
    snowflake_password: str | None = None
    snowflake_warehouse: str = "COMPUTE_WH"
    snowflake_database: str = "TREECARE"
    snowflake_schema: str = "MARTS"
    snowflake_role: str | None = None

    @property
    def snowflake_configured(self) -> bool:
        return all(
            [self.snowflake_account, self.snowflake_user, self.snowflake_password]
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
