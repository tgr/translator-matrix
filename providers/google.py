#!/usr/bin/env python

from typing import List

from .provider import Provider


class Google(Provider):
    """Language compatibility table for Google Cloud Translation API"""
    
    def fetch(self) -> List[str]:
        languages = []
        soup = self._get_soup()
        rows = soup.find('tbody').find_all('tr')
        for row in rows:
            language_code = row.find_all('td')[1].get_text().strip()
            languages.append(language_code)
        languages.sort()
        return languages
    
    def url(self) -> str:
        return 'https://cloud.google.com/translate/docs/languages'
