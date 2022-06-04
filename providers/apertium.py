#!/usr/bin/env python

import re
from typing import List

from bs4 import Tag

from .provider import Provider


class Apertium(Provider):
    """Language compatibility table for Apertium API"""

    def fetch(self) -> List[str]:
        # only fetch trunk languages for now
        languages = []
        soup = self._get_soup()
        trunk_section_title = soup.find(id='Trunk').parent
        trunk_table = None
        for sibling in trunk_section_title.next_siblings:
            if not isinstance(sibling, Tag):
                continue
            if re.search(r'^h\d$', sibling.name):
                break
            elif sibling.name == 'table':
                trunk_table = sibling
                break
        if not trunk_table:
            raise Exception('Trunk table not found')
        rows = trunk_table.find_all('tr')[1:]
        for row in rows:
            pair_name = row.find_all('td')[0].get_text().strip()
            m = re.match(r'apertium-(\w+)-(\w+)', pair_name)
            # FIXME Apertium only supports specific language pairs, not translation between any two of its supported languages
            languages.append(m[1])
            languages.append(m[2])
        languages = list(set(languages))
        languages.sort()
        return languages

    def url(self) -> str:
        return 'https://wiki.apertium.org/wiki/List_of_language_pairs'
