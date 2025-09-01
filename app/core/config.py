from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_NAME: str
    REDIS_HOST: str
    REDIS_PORT: str
    TOKEN_HERO: str
    BASE_URL_HERO: str = "https://superheroapi.com/api.php"

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # @property
    # def DATABASE_URL_psycopg(self):
    #     # DSN
    #     # postgresql+psycopg://postgres:postgres@localhost:5432/sa
    #     return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_TEST(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
