#!/usr/bin/env python

import sys
import argparse
import requests
import re
from bs4 import BeautifulSoup

# Parse CLI arguments
parser = argparse.ArgumentParser(description='Jisho CLI interface')
parser.add_argument('-n', '--num-of-results', type=int,\
        default=0, dest='max_results', help='Max amount of results')
parser.add_argument('-a', action='store_true',\
        help='Display alternative ways to write a word.')
parser.add_argument('search_terms', help='Search terms for Jisho.')
args = parser.parse_args()

source = requests.get('https://jisho.org/search/' + args.search_terms).text
matches = BeautifulSoup(source, 'lxml').find('div', id = 'primary')

if matches is None:
    print('No matches found.')
    exit(1)

result = []

# Loop through all results
for match in matches.find_all('div', class_ = 'concept_light clearfix'):

    if args.max_results != 0 and len(result) >= args.max_results:
        break

    # Get word + furigana
    # TODO: fix words with spaced out furigana
    word = match.find('div', class_ = 'concept_light-representation')
    word_furigana = word.find('span', class_ = 'furigana').text.strip()
    word_text = word.find('span', class_ = 'text').text.strip()

    # Get all meaning divs, prepary storage array
    meanings = match.find('div', class_ = 'concept_light-meanings')
    meanings_count = 1
    meanings_array = [word_text + (f' ({word_furigana})' if word_furigana else '')]

    for meaning in meanings.find_all('div', class_ = 'meaning-definition'):

        # TODO: add wiki entries?
        if meaning.find('span', class_ = 'meaning-abstract') is not None:
            continue

        meaning_span = meaning.find('span', class_ = 'meaning-meaning')

        # Ignore notes on okurigana usage
        if not meaning_span:
            continue

        # Separate meaning entries from "Other forms" entry
        if meaning_span.find('span', class_ = 'break-unit') is None:
            meanings_array.append(f'{meanings_count}: {meaning_span.text}')
            meanings_count += 1
        elif args.a:
            meanings_array.append(f'Other forms: {meaning_span.text}')

    # Append to result array
    if len(meanings_array) > 1:
        result.append('\n'.join(meanings_array))

print('\n\n'.join(result))
