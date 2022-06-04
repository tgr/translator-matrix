#!/usr/bin/env python

import re
from typing import List

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .provider import Provider


class DeepL(Provider):
    """Language compatibility table for DeepL API"""

    def fetch(self) -> List[str]:
        languages = []
        load_condition = EC.presence_of_element_located((By.CSS_SELECTOR, '[class^=table-module]'))
        soup = self._get_dynamic_soup(load_condition)
        source_lang_row = soup.find(class_=re.compile(r'^table-module')).find_all('tr')[2]
        if source_lang_row.find_all('td')[0].get_text().strip() != 'source_lang':
            raise Exception('Could not find source_lang documentation')
        lang_list = source_lang_row.find_all('td')[2].find('li')
        for lang_item in lang_list:
            language_code = re.search(r'"\w+"', lang_item.get_text())[0].lower()
            languages.append(language_code)
        languages.sort()
        return languages

    def url(self) -> str:
        return 'https://www.deepl.com/en/docs-api/translating-text/'
