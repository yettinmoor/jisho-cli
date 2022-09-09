#!/usr/bin/env python

import argparse
import requests
from bs4 import BeautifulSoup


class JishoEntry:

    def __init__(self, word, furigana):
        self.word = word
        self.furigana = furigana

        self.tags = []
        self.meanings = []
        self.other_forms = ''

    def __str__(self):
        s = self.word
        if self.furigana:
            s += f' ({self.furigana})'
        if self.tags:
            s += f' <{", ".join(self.tags)}>'
        s += '\n' + '\n'.join([f'{i}. {d}' for i, d in enumerate(self.meanings, 1)])
        if self.other_forms:
            s += '\nOther forms: ' + self.other_forms
        return s


def jisho_search(search_terms, max_results, force_romaji):
    if force_romaji:
        search_terms = f'"{search_terms}"'

    source = requests.get(f'https://jisho.org/search/{search_terms}').text
    matches = BeautifulSoup(source, 'lxml').find('div', id = 'primary')

    found_entries = []

    # Loop through all results
    for match in matches.find_all('div', class_ = 'concept_light clearfix'):

        if max_results != 0 and len(found_entries) >= max_results:
            break

        # Get word + furigana
        word = match.find('div', class_ = 'concept_light-representation')
        word_furigana = word.find('span', class_ = 'furigana').text.strip()
        word_text = word.find('span', class_ = 'text').text.strip()

        # Create entry object
        new_entry = JishoEntry(word_text, word_furigana)

        # Get "Common word" and JLPT tags
        for tag in match.find_all('span', class_ = 'concept_light-tag'):
            if tag.text == 'Common word':
                new_entry.tags.append('Common')
            elif tag.text.startswith('JLPT'):
                new_entry.tags.append(tag.text.split(' ')[-1])

        # Loop through meanings in entry
        meanings = match.find('div', class_ = 'concept_light-meanings')
        for meaning in meanings.find_all('div', class_ = 'meaning-definition'):

            # Ignore wiki entries
            if meaning.find('span', class_ = 'meaning-abstract') is not None:
                continue

            meaning_span = meaning.find('span', class_ = 'meaning-meaning')

            # Ignore notes on okurigana usage
            if not meaning_span:
                continue

            meaning_text = meaning_span.text

            # Find supplementary info e.g. written in kana, polite language, etc.
            supplement_span = meaning.find('span', class_ = 'supplemental_info')
            if supplement_span:
                sup_list = 'Kana/Neg/Polite/Humble/Honorific/Colloq/Slang/Vulgar/Derogatory'
                supplements = [sup for sup in sup_list.split('/') if sup.lower() in supplement_span.text]
                if supplements:
                    meaning_text += f' <{", ".join(supplements)}>'

            # Separate meaning entries from "Other forms" entry
            if meaning_span.find('span', class_ = 'break-unit') is None:
                new_entry.meanings.append(meaning_text)
            else:
                new_entry.other_forms = meaning_text

        # Add to result list
        if new_entry.meanings:
            found_entries.append(new_entry)

    return found_entries


def result_as_str(results):
    return '\n\n'.join(map(str, results)) or 'No matches found.'


def parser(args):
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Jisho CLI interface')
    parser.add_argument('-n', '--num-of-results', type=int,\
            default=0, dest='max_results', help='Max amount of results')
    parser.add_argument('-r', action='store_true',\
            dest='force_romaji', help='Always interpret search terms as English (Romaji) letters.')
    parser.add_argument('search_terms', help='Search terms for Jisho.')
    return parser.parse_args(args) if args else parser.parse_args()


def main(args_=None):
    args = parser(args_)
    result = jisho_search(args.search_terms, args.max_results, args.force_romaji)
    print(result_as_str(result))


if __name__ == '__main__':
    main()
