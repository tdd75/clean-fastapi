import gettext
import logging

from fastapi import Header

from app import setting

logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, accept_language: str = Header(setting.DEFAULT_LOCALE, alias='Accept-Language')) -> None:
        self.accept_language = accept_language
        self.set_lang(accept_language)

    def set_lang(self, lang: str) -> None:
        try:
            self.translation = gettext.translation(
                'messages',
                localedir='app/infrastructure/locale',
                languages=[lang],
                fallback=True,
            )
        except Exception as e:
            logger.warning(f"Translation error for language '{lang}': {e}")

    def translate(self, msg: str) -> str:
        return self.translation.gettext(msg)
