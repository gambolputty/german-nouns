# German nouns
A sqlite database table of ~ 83 thousand german nouns and their grammatical properties (*tense, number, gender*).

More info about the different columns can be found [here](https://de.wiktionary.org/wiki/Hilfe:Flexionstabellen)

Compiled from [WiktionaryDE](https://de.wiktionary.org)

License: [Creative Commons Attribution-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/deed.en).

Setup:
- Install Anaconda
- Open Anaconda Shell and select path where README.md is located
- Create environment by: conda create --name german-nouns
- Activate environment by: conda activate german-nouns
- Install requests: conda install requests
- Check python version: python -v (should be at least python 3.8.0 now)
- Install bz2file: conda install bz2file
- Install lxml: conda install lxml
- Install pyphen: python -m pip install pyphen
- Call: python ./create_csv/main.py or python ./create_db/main.py