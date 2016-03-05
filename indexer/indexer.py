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


def build_es_document(word):
	dict = {}
	for letter in word.lower():
		if letter in dict:
			dict[letter] = dict[letter] + 1
		else:
			dict[letter] = 1
	
	return {
			'word' : word,
			'letters' : list(word.lower()),
			'length' : len(word),
			'dict' : dict
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
	counter = 1
	actions = []
	with open(args.dictionary) as f:	    
	    for line in f:
	    	word = line.decode(args.dict_encoding).strip()
	    	doc = build_es_document(word)
	    	action = build_es_action(args.index, args.type, counter, doc)
	    	actions.append(action)            
	    	counter = counter + 1
	    	if len(actions) > 500:
			helpers.bulk(es, actions)
			actions = []		
			print 'Indexed documents:: ', counter
		
	helpers.bulk(es, actions)
	print 'Indexed documents: ', counter


def main():
    parser = create_parser()
    args = parser.parse_args()
    es = setup_es(args.es_host, args.es_port, args.index, args.delete_index)
    index(args, es)


if __name__ == '__main__':
    main()
