# Hexson

[![Python version](https://img.shields.io/pypi/pyversions/hexson.svg)](https://pypi.org/project/hexson)
[![Build Status](https://travis-ci.org/wonderqs/hexson.svg?branch=master)](https://travis-ci.org/wonderqs/hexson)
[![PyPI version](https://badge.fury.io/py/hexson.svg)](https://badge.fury.io/py/hexson)

Json library designed for binary data processing.

Different from built-in json library, Hexson can encode invisible characters 
with hex escape instead of unicode escape.

## Install

````
pip3 install hexson
````

## Usage

### loader & dumpper

````
json_dict = hexson.load(fd)
json_str = hexson.dump(json_dict, fd)
````

### Elasticsearch serializer

````
es_conn = elasticsearch.Elasticsearch([{'host': cfg['es']['host'], 'port': cfg['es']['port']}],
                                          http_auth=(cfg['es']['user'], cfg['es']['pass']),
                                          timeout=60, serializer=hexson.JSONSerializer())
````
