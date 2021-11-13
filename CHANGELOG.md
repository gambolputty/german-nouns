# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2021-11-13
### Added
- Tests

### Changed
- Converted repository to [Poetry](https://python-poetry.org/) project
- Rename repository and package from `german_nouns` to `german-nouns`.
- Rename `NounDictionary` to `Nouns`

### Removed
- `last_word` method

### Fixed
- Some parsing improvements due to `wiktionary-de-parser` update

## [1.1.0] - 2020-07-29
### Added
- Add `exclude_lemmas` option when querying compounds

## [1.1.0] - 2020-07-08
### Added
- `setup.sh` to install all package requirements
- methods for querying the nouns file (see `german_nouns/query`)
### Changed
- directory structure
- README.md

## [1.0.1] - 2020-07-06
### Added
- [wiktionary_de_parser](https://github.com/gambolputty/wiktionary_de_parser) requirement

### Changed
- updated `create_csv/main.py` to use with latest version of [wiktionary_de_parser](https://github.com/gambolputty/wiktionary_de_parser)
- updated `nouns.csv`
- README

## [1.0.0] - 2019-04-14
### Added
- [wiktionary_de_parser](https://github.com/gambolputty/wiktionary_de_parser) as parser script for Wiktionary xml dump
- 'Genus 1' - 'Genus 4' columns

### Fixed
- overall better parsing results due to submodule [wiktionary_de_parser](https://github.com/gambolputty/wiktionary_de_parser)

### Changed
- Python 3.7+ requirement

### Removed
- compound column due to unprecise results

## [0.9.0] - 2018-06-11
### Fixed
- remove dashes in empty cells

## [0.8.0] - 2018-05-29
### Added
- info about compound words

### Fixed
- improved parser script (+11 thousand more nouns)

## [0.7.0] - 2017-08-29
### Added
- prefill declination values for adjective nouns

### Fixed
- sorting order in nouns.csv

### Changed
- refactor parser script
- updated readme
- column 'WikiTitel' to 'lemma'

## [0.6.0] - 2017-08-17
### Changed
- refactor code

### Fixed
- improved noun parsing
- fixed dash chracter for non-available singulars or plurals

## [0.5.0] - 2017-01-24
### Added
- initial release