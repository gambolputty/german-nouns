#!/bin/bash
set -x

# install requirements
pip install -r ./requirements.txt

# install spacy model
python3 -m spacy download de_core_news_sm