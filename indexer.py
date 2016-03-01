import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch([{"host":"XXX", "port":80}])
es.indices.delete("_all")

# ignore 400 cause by IndexAlreadyExistsException when creating an index

index = "german"
type = "word"

es.indices.create(index=index, ignore=400)


counter = 1
actions = []
with open("german.dic") as f:	    
    for line in f:
    	word = line.decode("latin-1").strip()
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
		"_index" : index,
		"_type" : type,
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

