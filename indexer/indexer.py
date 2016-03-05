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
	parser.add_argument('--dictionary', default='../data/german.dic', help='Path to dictionary file, default = ../data/german.dic')
	parser.add_argument('--dict_encoding', default='latin-1', help='Dictionary file encoding, default = latin-1')
	parser.add_argument('--delete_index', action='store_true', default=False, help='Drop index before indexing?, default = False')
	return parser

def doStuff(args):
	# elasticsarch setup
	es = Elasticsearch([{"host":args.es_host, "port":args.es_port}])
	if args.delete_index:
		es.indices.delete(args.index)
	# ignore 400 cause by IndexAlreadyExistsException when creating an index
	es.indices.create(index=args.index, ignore=400)


	counter = 1
	actions = []
	with open(args.dictionary) as f:	    
	    for line in f:
	    	word = line.decode(args.dict_encoding).strip()
		dict = {}
		for letter in word.lower():
			if letter in dict:
				dict[letter] = dict[letter] + 1
			else:
				dict[letter] = 1
		
	      	doc = {
				"word" : word,
				"letters" : list(word.lower()),
				"length" : len(word),
				"dict" : dict
			}
		action = {
			"_index" : args.index,
			"_type" : args.type,
	          	"_id" : counter,
			"_source" : doc
			}
		actions.append(action)            
		counter = counter + 1

		if len(actions) > 500:
			output = helpers.bulk(es, actions)
			actions = []		
			# print json.dumps(doc)
	        	# output = es.index(index="german", doc_type="word", body=doc)
			print output	
			print "counter: ", counter

def main():
    parser = create_parser()
    args = parser.parse_args()
    doStuff(args)

if __name__ == '__main__':
    main()