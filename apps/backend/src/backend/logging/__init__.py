import logging.config
from pathlib import Path

from ..core.types import Environment
from .config import LoggingConfig, logging_config
from .log_config import build_log_config


def setup_logging(
    environment: Environment, config: LoggingConfig = logging_config
) -> None:
    """Configures logging based on the provided settings."""
    is_prod = environment == Environment.PRODUCTION

    if is_prod and not config.LOG_DIR:
        raise RuntimeError("LOG_DIR must be set in production environment")

    log_path = Path(config.LOG_DIR)
    if not log_path.is_dir():
        log_path.mkdir(parents=True, exist_ok=True)

    log_config = build_log_config(environment, config)
    logging.config.dictConfig(log_config)
