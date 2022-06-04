#!/usr/bin/env python

from typing import List

from .provider import Provider


class Amazon(Provider):
    """Language compatibility table for Amazon Translate API"""
    
    def fetch(self) -> List[str]:
        languages = []
        soup = self._get_soup()
        rows = soup.find('table').find_all('tr')[1:]
        for row in rows:
            language_code = row.find_all('td')[1].get_text().strip()
            languages.append(language_code)
        languages.sort()
        return languages

    def url(self) -> str:
        return 'https://docs.aws.amazon.com/translate/latest/dg/what-is-languages.html'
