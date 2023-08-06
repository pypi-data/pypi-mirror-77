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

Serialize from / Deserialize to file:

````python
json_dict = hexson.load(fd)
hexson.dump(json_dict, fd)
````

Serialize from / Deserialize to string:

````python
json_dict = hexson.loads(json_string)
json_string = hexson.dumps(json_dict)
````

Function `load` and `loads` will parse string in Json to *bytes* in Python by default.
And you can convert it into string in Python by set parameter `utf_8_string` to `True`, just like:

````python
json_dict = hexson.load(fd, utf_8_string=True)
json_dict = hexson.loads(json_string, utf_8_string=True)
````

### Elasticsearch serializer

Hexson can work along with official `elasticsearch` Python client library.

````python
import elasticsearch

hexson_serializer = hexson.JSONSerializer()
es_conn = elasticsearch.Elasticsearch(serializer=hexson_serializer)
````
