# Phonetizer - French

Utils library that converts French word or text into phonems.
Provides python functions and CLI.

## Usage

Install as pip package, then use command line:
```
$ sentence_to_phonem maison
-> mEz§
```

## GCP API
In Process...

## Under the cogs

- Cuts sentence into words
- Checks if word is in dictionary
- If so returns phonemic translation
- Else returns WordNotFoundError

## Dev

To dev in local while retaining access to GCP:
```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcp/jsons/phonetizer-dev-key.json
```

## Todo

- Lib for nn inference of unknown words is up. Needs to be faster (preload model before inference). Use it to guess new words.
- Parse Wiktionaire for more comprehensive dictionary
- Create POS-Tagging to resolve non-homophonic homograms 
