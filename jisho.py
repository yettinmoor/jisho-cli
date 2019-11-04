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

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_meaning(self, meaning):
        self.meanings.append(meaning)

    def add_other(self, other_forms):
        self.other_forms = other_forms

    def is_empty(self):
        return not self.meanings

    def as_str(self, display_other):
        entry_str = self.word
        if self.furigana:
            entry_str += f' ({self.furigana})'
        if self.tags:
            entry_str += f' <{", ".join(self.tags)}>'

        entry_str += '\n' + '\n'.join([f'{i+1}. {d}' for i, d in enumerate(self.meanings)])

        if display_other and self.other_forms:
            entry_str += '\nOther forms: ' + self.other_forms

        return entry_str


def jisho_search(search_terms, max_results):
    source = requests.get('https://jisho.org/search/' + search_terms).text
    matches = BeautifulSoup(source, 'lxml').find('div', id = 'primary')

    result = []

    # Loop through all results
    for match in matches.find_all('div', class_ = 'concept_light clearfix'):

        if max_results != 0 and len(result) >= max_results:
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
                new_entry.add_tag('Common')
            elif tag.text.startswith('JLPT'):
                new_entry.add_tag(tag.text.split(' ')[-1])

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
                sup_text = supplement_span.text
                sup_list = 'kana/Polite/Humble/Honorific/Colloq/Slang/Vulgar/Derogatory'
                supplements = []
                for sup in sup_list.split('/'):
                    if sup in sup_text:
                        supplements.append(sup.title())
                if supplements:
                    meaning_text += f' <{", ".join(supplements)}>'

            # Separate meaning entries from "Other forms" entry
            if meaning_span.find('span', class_ = 'break-unit') is None:
                new_entry.add_meaning(meaning_text)
            else:
                new_entry.add_other(meaning_text)

        # Add to result list
        if not new_entry.is_empty():
            result.append(new_entry)

    return result


def print_search(search_result, display_other):
    if not search_result:
        print('No matches found.')
    else:
        print('\n\n'.join(map(lambda r: r.as_str(display_other), search_result)))


if __name__ == '__main__':

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Jisho CLI interface')
    parser.add_argument('-n', '--num-of-results', type=int,\
            default=0, dest='max_results', help='Max amount of results')
    parser.add_argument('-a', action='store_true',\
            dest='display_other', help='Display alternative ways to write a word.')
    parser.add_argument('search_terms', help='Search terms for Jisho.')
    args = parser.parse_args()

    result = jisho_search(args.search_terms, args.max_results)
    print_search(result, args.display_other)
