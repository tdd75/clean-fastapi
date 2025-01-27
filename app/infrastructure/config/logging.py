import logging

from app.infrastructure.config.setting import Setting


def config_logging(setting: Setting) -> None:
    logging.basicConfig(
        level=setting.LOG_LEVEL,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s (%(pathname)s:%(lineno)d)',
    )
