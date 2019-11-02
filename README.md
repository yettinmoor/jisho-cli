# A simple Jisho web scraper

A CLI interface to the popular [Jisho Japanese web dictionary](https://jisho.org). Written in Python with BeautifulSoup API.

## Todo

* Kanji page (e.g. `jisho -k 恋`)
* Links to pronounciation audio files

## Examples

```
$ jisho nihongo
日本語(にほんご)
1: Japanese (language)

日本語能力試験(にほんごのうりょくしけん)
1: Japanese Language Proficiency Test; JLPT

[etc.]
```

```
$ jisho 走る
走る(はし)
1: to run
2: to travel (movement of vehicles); to drive; to flow (e.g. energy)
3: to hurry to
4: to retreat (from battle); to take flight
5: to run away from home
6: to elope
7: to tend heavily toward
8: to flash; to streak; to shoot through (e.g. pain)
```
