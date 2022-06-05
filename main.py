#!/usr/bin/env python
"""Generate language support tables for common translation APIs"""

import csv
import sys
import argparse

import langcodes
from langcodes import Language, LanguageTagError

from providers import Google, Microsoft, DeepL, Amazon, Yandex, Apertium, LibreTranslate


def handle_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider', type=str, help='Only fetch this provider (for debugging). Use lowercase.')
    parser.add_argument('--file', type=str, help='Filename to write CSV to (defaults to stdout).')
    return parser.parse_args()


def normalize_languages(language_list):
    normalized_language_list = []
    for lang in language_list:
        # Google has some human-readable junk in the list
        lang = lang.split(' ')[0]
        try:
            lang = langcodes.standardize_tag(lang)
        except LanguageTagError:
            pass
        normalized_language_list.append(lang)
    return set(normalized_language_list)


def main():
    args = handle_args()

    data = {}
    data_by_language = {}
    providers = [
        Google(),
        Microsoft(),
        DeepL(),
        Amazon(),
        Yandex(),
        Apertium(),
        LibreTranslate()
    ]
    if args.provider:
        providers = list(filter(lambda p: p.name().lower() in args.provider, providers))
        if not providers:
            raise Exception('Unknown provider')
    languages = set()
    for provider in providers:
        supported_languages = normalize_languages(provider.fetch())
        data[provider.name()] = {
            "url": provider.url(),
            "languages": supported_languages,
        }
        languages.update(supported_languages)
    languages = list(languages)
    languages.sort()
    for lang in languages:
        data_by_language[lang] = {}
        for provider in providers:
            if lang in data[provider.name()]['languages']:
                data_by_language[lang][provider.name()] = '✓'
            else:
                data_by_language[lang][provider.name()] = ''

    output = sys.stdout
    if args.file:
        output = open(args.file, 'w')
    writer = csv.writer(output, dialect='unix')
    header = ['', '', '']
    header.extend(f'=HYPERLINK("{provider.url()}", "{provider.name()}")' for provider in providers)
    writer.writerow(header)
    for lang_code, lang_data in data_by_language.items():
        try:
            lang = Language.get(lang_code)
            row = [lang.to_tag(), lang.display_name(), lang.autonym()]
        except LanguageTagError:
            row = [lang_code, '', '']
        row.extend(lang_data.values())
        writer.writerow(row)


if __name__ == "__main__":
    main()