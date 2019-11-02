#!/usr/bin/env python

import sys
import requests
import re
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print('Usage: jisho [search terms]')
    exit(1)

# TODO
display_other_forms = False

search_terms = ' '.join(sys.argv[1:])

source = requests.get('https://jisho.org/search/' + search_terms).text
soup = BeautifulSoup(source, 'lxml')

matches = soup.find('div', id = 'primary')

if matches is None:
    print('No matches found.')
    exit(1)

result = []

# Loop through all results
for match in matches.find_all('div', class_ = 'concept_light clearfix'):

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
        elif display_other_forms:
            meanings_array.append(f'Other forms: {meaning_span.text}')

    # Append to result array
    if len(meanings_array) > 1:
        result.append('\n'.join(meanings_array))

print('\n\n'.join(result))
