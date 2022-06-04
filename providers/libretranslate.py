#!/usr/bin/env python

from typing import List

from .provider import Provider


class LibreTranslate(Provider):
    """Language compatibility table for LibreTranslate API"""

    def fetch(self) -> List[str]:
        # very short list and no language codes, not worth bothering with
        return ['en', 'ar', 'zh', 'fr', 'de', 'it', 'ja', 'pt', 'ru', 'es']

    def url(self) -> str:
        return 'https://docs.rs/libretranslate/0.2.2/libretranslate/index.html#available-languages'
