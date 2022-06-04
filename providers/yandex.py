#!/usr/bin/env python

from typing import List

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .provider import Provider


class Yandex(Provider):
    """Language compatibility table for Yandex Translate API"""

    def fetch(self) -> List[str]:
        languages = []
        load_condition = EC.presence_of_element_located((By.CSS_SELECTOR, 'ol'))
        soup = self._get_dynamic_soup(load_condition)
        list = soup.find_all('ol')[1]
        for list_item in list.find_all('li'):
            language_code = list_item.find('code').get_text().strip()
            languages.append(language_code)
        languages.sort()
        return languages

    def url(self) -> str:
        return 'https://cloud.yandex.com/en/docs/translate/concepts/supported-languages'
