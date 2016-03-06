import pytest
from indexer import indexer

def test_simple_action():
    doc = {
            'word' : 'Haus',
            'letters' : ['h', 'a', 'u', 's'],
            'length' : 4,
            'dict' : {
                'h' : 1,
                'a' : 1,
                'u' : 1,
                's' : 1
            }
    }

    action = indexer.build_es_action('index', 'type', 111, doc)

    assert action['_index'] == 'index'
    assert action['_type'] == 'type'
    assert action['_id'] == 111
    assert action['_source'] == doc
