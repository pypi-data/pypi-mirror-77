# TAPCODE

[![PyPI version](https://badge.fury.io/py/tapcode.svg)](https://badge.fury.io/py/tapcode) [![Requirements Status](https://requires.io/github/remiflavien1/tapcode/requirements.svg?branch=master)](https://requires.io/github/remiflavien1/tapcode/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/tapcode/badge/?version=latest)](https://tapcode.readthedocs.io/en/latest/?badge=latest)


Tapcode Cypher also known as Prisoner's tapcode.
For a complete documentation look at [ReadTheDocs](https://tapcode.readthedocs.io/en/latest/)


# Install

You can install ```tapcode``` either via pip (PyPI) or from source.
To install using pip:
```bash
pip3 install tapcode
```
Or manually:
```
git clone https://github.com/remiflavien1/tapcode
cd tapcode
python3 setup.py install
```

## CLI
```
$ tapcode --help 

usage: tapcode [-h] [-s SENTENCE] [-f FILE] [-d] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -s SENTENCE, --sentence SENTENCE
                        Sentence to cypher or decipher
  -f FILE, --file FILE  file to cypher or decipher
  -d, --decode          decode tapcode sentence.
  -e, --encode          encode sentences to tapcode.
```


Encipher a clear message : 
```sh
$ tapcode -es "I Love Tapcode"
24 31345115 44113513341415.
```

Decipher a tapcode message :
```sh
$tapcode -ds "24 31345115 44113513341415"
I LOVE TAPCODE .
```

You can do the same but from file :

```sh
# Encipher
$ echo "I love coffee !" > to_encode.txt
$ tapcode -ef to_encode.txt
$ cat encoded
24 31345115 133421211515 .

# Decipher
$ echo "24 31345115 3511434411" > to_decode.txt
$ tapcode -df to_decode.txt
$ cat decoded
I LOVE PASTA .
```

# API

For a complete API documentation look at [ReadTheDocs](https://tapcode.readthedocs.io/en/latest/)

```