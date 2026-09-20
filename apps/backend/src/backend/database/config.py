from backend.common.config import CustomBaseSettings


class DatabaseConfig(CustomBaseSettings):
    model_config = {
        **CustomBaseSettings.model_config,
        "env_prefix": "DB_",
    }

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    NAME: str = "db"
    DRIVER: str = "asyncpg"

    POOL_SIZE: int = 20
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    MAX_OVERFLOW: int = 10
    PREFIXED_ID_LENGTH: int = 21

    @property
    def DB_URL(self) -> str:
        return f"postgresql+{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    @property
    def POSTGRES_INDEXES_NAMING_CONVENTION(self) -> dict[str, str]:
        return {
            "ix": "%(column_0_label)s_idx",
            "uq": "%(table_name)s_%(column_0_name)s_uq",
            "ck": "%(table_name)s_%(constraint_name)s_check",
            "fk": "%(table_name)s_%(column_0_name)s_fkey",
            "pk": "%(table_name)s_pkey",
        }


db_config = DatabaseConfig()
