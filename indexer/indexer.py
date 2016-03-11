#!/usr/bin/python
# -*- coding: utf-8-*-

import argparse
from elasticsearch import Elasticsearch, helpers


def create_parser():
    parser = argparse.ArgumentParser(description='Index words to elasticsearch.')
    parser.add_argument('--es_host', default='localhost', help='Hostname of elasticsearch, default = localhost')
    parser.add_argument('--es_port', type=int, default=9200, help='Hostname of elasticsearch, default = 9200')
    parser.add_argument('--index', default='german', help='Name of index, default = german')
    parser.add_argument('--type', default='word', help='Type of indexed documents, default = word')
    parser.add_argument('--dictionary', default='data/german.dic',
                        help='Path to dictionary file, default = data/german.dic')
    parser.add_argument('--dict_encoding', default='latin-1', help='Dictionary file encoding, default = latin-1')
    parser.add_argument('--delete_index', action='store_true', default=False,
                        help='Drop index before indexing?, default = False')
    return parser


def build_dict_from_word(word):
    letter_dict = {}
    for letter in word.lower():
        if letter in letter_dict:
            letter_dict[letter] += 1
        else:
            letter_dict[letter] = 1
    return letter_dict


def build_es_document(word, encoding):
    word = word.decode(encoding).strip()
    return {
        'word': word,
        'letters': list(word.lower()),
        'length': len(word),
        'dict': build_dict_from_word(word)
    }


def build_es_action(es_index, doc_type, doc_id, doc):
    return {
        '_index': es_index,
        '_type': doc_type,
        '_id': doc_id,
        '_source': doc
    }


def setup_es(host, port, es_index, delete_index):
    print 'Setting up connection to elasticsearch on %s:%s' % (host, port)
    es = Elasticsearch([{'host': host, 'port': port}])
    if delete_index:
        print 'Deleting index %s...' % es_index
        es.indices.delete(es_index)
    # ignore 400 cause by IndexAlreadyExistsException when creating an index
    print 'Creating index %s...' % es_index
    es.indices.create(index=index, ignore=400)
    return es


def print_progress(indexed_so_far, all_docs):
    percent = indexed_so_far * 100 / all_docs
    print 'Indexed documents: %d from %d, progress: %.f%%' % (indexed_so_far, all_docs, percent)


def index(args, es):
    with open(args.dictionary) as dict_file:
        print 'Counting number of lines in %s ...' % dict_file.name
        num_lines = sum(1 for line in dict_file)
        dict_file.seek(0)
        indexed_counter = 0
        es_actions = []

        for line in dict_file:
            doc = build_es_document(line, args.dict_encoding)
            es_action = build_es_action(args.index, args.type, indexed_counter, doc)
            es_actions.append(es_action)
            indexed_counter += 1
            if len(es_actions) >= 500:
                print "Indexing batch..."
                helpers.bulk(es, es_actions)
                es_actions = []
                print_progress(indexed_counter, num_lines)

        # index remaining docs
        print "Indexing batch..."
        helpers.bulk(es, es_actions)
        print_progress(indexed_counter, num_lines)


def main():
    parser = create_parser()
    args = parser.parse_args()
    es = setup_es(args.es_host, args.es_port, args.index, args.delete_index)
    index(args, es)


if __name__ == '__main__':
    main()
