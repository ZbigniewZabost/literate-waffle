# -*- coding: utf-8-*-
import pytest
from indexer import indexer

def test_simple_word():
	doc = indexer.build_es_document('Haus')
	assert doc['word'] == 'Haus'
	assert doc['letters'] == ['h', 'a', 'u', 's']
	assert doc['length'] == 4
	assert doc['dict'] == {'h' : 1, 'a' : 1, 'u' : 1, 's' : 1}


def test_word_with_duplicated_letters():
	doc = indexer.build_es_document('See')
	assert doc['word'] == 'See'
	assert doc['letters'] == ['s', 'e', 'e']
	assert doc['length'] == 3
	assert doc['dict'] == {'s' : 1, 'e' : 2}


@pytest.mark.skip(reason='fix me: special letters not handled properly')
def test_word_with_special_letters():
	doc = indexer.build_es_document('Maß')
	assert doc['word'] == 'Maß'
	assert doc['letters'] == ['M', 'a', 'ß']
	assert doc['length'] == 3
	assert doc['dict'] == {'m' : 1, 'a' : 1, 'ß': 1}