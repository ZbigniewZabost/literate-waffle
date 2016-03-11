from indexer import indexer


def test_all_defaults():
    parser = indexer.create_parser()
    args = parser.parse_args()
    assert args.es_host == 'localhost'
    assert args.es_port == 9200
    assert args.index == 'german'
    assert args.type == 'word'
    assert args.dictionary == 'data/german.dic'
    assert args.dict_encoding == 'latin-1'
    assert args.delete_index is False


def test_no_defaults():
    parser = indexer.create_parser()
    args = parser.parse_args('--es_host host --es_port 1111 --index index --type type '
                             '--dictionary dic --dict_encoding utf-8 --delete_index'.split())
    assert args.es_host == 'host'
    assert args.es_port == 1111
    assert args.index == 'index'
    assert args.type == 'type'
    assert args.dictionary == 'dic'
    assert args.dict_encoding == 'utf-8'
    assert args.delete_index is True


def test_some_defaults():
    parser = indexer.create_parser()
    args = parser.parse_args('--es_host host --dict_encoding utf-8 --delete_index'.split())
    assert args.es_host == 'host'
    assert args.es_port == 9200
    assert args.index == 'german'
    assert args.type == 'word'
    assert args.dictionary == 'data/german.dic'
    assert args.dict_encoding == 'utf-8'
    assert args.delete_index is True
