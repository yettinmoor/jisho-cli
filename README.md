# Jisho

A Python CLI interface to [Jisho](https://jisho.org).

## Usage

Type `jisho [search terms]`. Multiple-word searches should be enclosed in "quotations". Use `jisho -n [N]` to limit the number of results.

```
$ jisho -n 1 nihongo
日本語 (にほんご) <Common>
1: Japanese (language)
```

Tags are shown next to the word. `Common` connotes a commonly used word; `N1` to `N5` refers to JLPT level.

`jisho -a` will display alternate forms if any are found.

```
$ jisho -n 1 -a 恋
恋 (こい) <Common, N3>
1. (romantic) love
Other forms: 戀 【こい】、孤悲 【こい】
```

Tags are also displayed next to invidivual meanings. For example, `Kana` means that a word is usually written in hiragana/katakana as opposed to kanji when used with this meaning. Other tags include `Polite`, `Slang`, `Honorific`, etc.

If Romaji input can be transcribed into kana, Jisho will transcribe it. For example, `jisho made` will search for まで. Use `jisho -r` to force Romaji.

## Todo

* Kanji page (e.g. `jisho -k 恋`)
* Links to pronounciation audio files
