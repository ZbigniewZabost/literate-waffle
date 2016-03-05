# literate-waffle  [![Build Status](https://travis-ci.org/zbigniewz/literate-waffle.svg?branch=master)](https://travis-ci.org/zbigniewz/literate-waffle)
Index words to elasticsearch

```
python indexer.py -h
usage: indexer.py [-h] [--es_host ES_HOST] [--index INDEX] [--type TYPE]
                  [--dictionary DICTIONARY] [--delete_index DELETE_INDEX]

Index words to elasticsearch.

optional arguments:
  -h, --help            show this help message and exit
  --es_host ES_HOST     Hostname of elasticsearch, default = localhost
  --index INDEX         Name of index, default = german
  --type TYPE           Type of indexed documents, default = word
  --dictionary DICTIONARY
                        Path to dictionary file, default = german.dic
  --delete_index DELETE_INDEX
                        Drop index before indexing?, default = True
```
