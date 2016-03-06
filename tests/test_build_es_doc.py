# -*- coding: utf-8-*-
import pytest
from indexer import indexer

def test_simple_word():
	doc = indexer.build_es_document('Haus', 'utf-8')
	assert doc['word'] == 'Haus'
	assert doc['letters'] == ['h', 'a', 'u', 's']
	assert doc['length'] == 4
	assert doc['dict'] == {'h' : 1, 'a' : 1, 'u' : 1, 's' : 1}


def test_word_with_duplicated_letters():
	doc = indexer.build_es_document('See', 'utf-8')
	assert doc['word'] == 'See'
	assert doc['letters'] == ['s', 'e', 'e']
	assert doc['length'] == 3
	assert doc['dict'] == {'s' : 1, 'e' : 2}


def test_word_with_special_letters():
	doc = indexer.build_es_document('Maß', 'utf-8')
	assert doc['word'] == 'Maß'.decode('utf-8')
	assert doc['letters'][0] == 'm'
	assert doc['letters'][1] == 'a'
	assert doc['letters'][2] == 'ß'.decode('utf-8')
	assert doc['length'] == 3
	assert doc['dict'] == {'m' : 1, 'a' : 1, 'ß'.decode('utf-8'): 1}