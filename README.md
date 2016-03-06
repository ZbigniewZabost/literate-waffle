# literate-waffle: elasticsearch word indexer  [![Build Status](https://travis-ci.org/zbigniewz/literate-waffle.svg?branch=master)](https://travis-ci.org/zbigniewz/literate-waffle)

**Usage**

```
python indexer/indexer.py -h
usage: indexer.py [-h] [--es_host ES_HOST] [--es_port ES_PORT] [--index INDEX]
                  [--type TYPE] [--dictionary DICTIONARY]
                  [--dict_encoding DICT_ENCODING] [--delete_index]

Index words to elasticsearch.

optional arguments:
  -h, --help            show this help message and exit
  --es_host ES_HOST     Hostname of elasticsearch, default = localhost
  --es_port ES_PORT     Hostname of elasticsearch, default = 9200
  --index INDEX         Name of index, default = german
  --type TYPE           Type of indexed documents, default = word
  --dictionary DICTIONARY
                        Path to dictionary file, default = data/german.dic
  --dict_encoding DICT_ENCODING
                        Dictionary file encoding, default = latin-1
  --delete_index        Drop index before indexing?, default = False
```



**Example of indexed document**
```
{
  "_index": "germanv5",
  "_type": "word",
  "_id": "4",
  "_score": 1,
  "_source": {
    "letters": [
      "s",
      "p",
      "i",
      "e",
      "l",
      "e",
      "n"
    ],
    "length": 7,
    "word": "spielen",
    "dict": {
      "e": 2,
      "i": 1,
      "l": 1,
      "n": 1,
      "p": 1,
      "s": 1
    }
  }
}
```



**Downloadable list of german words**

https://sourceforge.net/projects/germandict/

