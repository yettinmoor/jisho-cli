#!/usr/bin/env python

import sys
import requests
import re
from bs4 import BeautifulSoup as bs

display_other_forms = False

if len(sys.argv) < 2:
    print('Usage: jisho [search terms]')

search_terms = ' '.join(sys.argv[1:])

source = requests.get('https://jisho.org/search/' + search_terms).text
jsoup = bs(source, 'lxml')

matches = jsoup.find('div', id = 'primary')

if matches is None:
    print('No matches found.')
    exit(1)

result = []

# Loop through all results
for match in matches.find_all('div', class_ = 'concept_light clearfix'):

    word = match.find('div', class_ = 'concept_light-representation')
    word_furigana = word.find('span', class_ = 'furigana').text.strip()
    word_kanji = word.find('span', class_ = 'text').text.strip()

    meanings = match.find('div', class_ = 'concept_light-meanings')
    meanings_count = 1
    meanings_array = [word_kanji + (f' ({word_furigana})' if word_furigana else '')]

    for meaning in meanings.find_all('div', class_ = 'meaning-definition'):

        # Avoid wiki
        if meaning.find('span', class_ = 'meaning-abstract') is not None:
            continue

        meaning_text = meaning.find('span', class_ = 'meaning-meaning')
        if not meaning_text:
            continue

        if meaning_text.find('span', class_ = 'break-unit') is None:
            meanings_array.append(f'{meanings_count}: {meaning_text.text}')
            meanings_count += 1
        elif display_other_forms:
            meanings_array.append(f'Other forms: {meaning_text.text}')

    # Print
    if len(meanings_array) > 1:
        result.append('\n'.join(meanings_array))

print('\n\n'.join(result))
