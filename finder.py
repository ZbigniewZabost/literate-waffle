#!/usr/bin/python
# -*- coding: utf-8-*-

import json
from elasticsearch import Elasticsearch
es = Elasticsearch([{"host":"XXX", "port":80}])

letters = "hzrashawocop"
size = 7


body = {
	"from" : 0, "size" : 1000,
	"fields" : ["word"],
	"query" : {
  		"filtered": {
    		"query": {
				"regexp":{
					"word": "[" + letters + "]{" + str(size) + "}"
				}
    		},
    		"filter": {
    			"term" : {
    				"length": size
    			}
    		}
  		}
	}
}

output = es.search("german", "word", body)

filter_dict = {}

for c in letters:
	if c in filter_dict:
		filter_dict[c] = filter_dict[c] + 1
	else:
		filter_dict[c] = 1

print filter_dict

all_words = []
correct_words = []

for element in output["hits"]["hits"]:
    all_words.append(element["fields"]["word"][0])

print all_words

for w in all_words:
	matched = True
	word = w.lower();
	for key, value in filter_dict.iteritems():
		if word.count(key) > value:
			matched = False
	if matched == True:
		correct_words.append(w)

print len(correct_words)

for w in correct_words:
	print w



