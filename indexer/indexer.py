#!/usr/bin/python
# -*- coding: utf-8-*-

import json
import argparse
from elasticsearch import Elasticsearch, helpers


def create_parser():
	parser = argparse.ArgumentParser(description='Index words to elasticsearch.')
	parser.add_argument('--es_host', default='localhost', help='Hostname of elasticsearch, default = localhost')
	parser.add_argument('--es_port', type=int, default=9200, help='Hostname of elasticsearch, default = 9200')
	parser.add_argument('--index', default='german', help='Name of index, default = german')
	parser.add_argument('--type', default='word', help='Type of indexed documents, default = word')
	parser.add_argument('--dictionary', default='data/german.dic', help='Path to dictionary file, default = data/german.dic')
	parser.add_argument('--dict_encoding', default='latin-1', help='Dictionary file encoding, default = latin-1')
	parser.add_argument('--delete_index', action='store_true', default=False, help='Drop index before indexing?, default = False')
	return parser


def build_dict_from_word(word):
	dict = {}
	for letter in word.lower():
		if letter in dict:
			dict[letter] = dict[letter] + 1
		else:
			dict[letter] = 1
	return dict	


def build_es_document(word, encoding):
	word = word.decode(encoding).strip()
	return {
			'word' : word,
			'letters' : list(word.lower()),
			'length' : len(word),
			'dict' : build_dict_from_word(word)
		}


def build_es_action(index, doc_type, doc_id, doc):
	return {
			'_index' : index,
			'_type' : doc_type,
			'_id' : doc_id,
			'_source' : doc
		}


def setup_es(host, port, index, delete_index):
	es = Elasticsearch([{'host':host, 'port':port}])
	if delete_index:
		es.indices.delete(index)
	# ignore 400 cause by IndexAlreadyExistsException when creating an index
	es.indices.create(index=index, ignore=400)
	return es	


def index(args, es):
	indexed_counter = 0
	es_actions = []
	with open(args.dictionary) as dict_file:	    
	    for line in dict_file:
	    	doc = build_es_document(line, args.encoding)
	    	es_action = build_es_action(args.index, args.type, counter, doc)
	    	es_actions.append(es_action)            
	    	indexed_counter = indexed_counter + 1
	    	if len(es_actions) > 500:
			helpers.bulk(es, es_actions)
			actions = []		
			print 'Indexed documents: ', indexed_counter
	# index remaing docs	
	helpers.bulk(es, actions)
	print 'Indexed documents: ', indexed_counter


def main():
    parser = create_parser()
    args = parser.parse_args()
    es = setup_es(args.es_host, args.es_port, args.index, args.delete_index)
    index(args, es)


if __name__ == '__main__':
    main()
