from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    bot_token: str = Field(min_length=1)
    database_url: str = "sqlite+aiosqlite:///./bot.db"
    captcha_ttl_seconds: int = 30
    captcha_max_attempts: int = 3
    admin_user_ids: str = ""
    mini_app_url: str = "https://miniapptg.kirillfomenkov92.workers.dev/"
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def admin_ids(self) -> set[int]:
        return {int(x.strip()) for x in self.admin_user_ids.split(",") if x.strip()}
