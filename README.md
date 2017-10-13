# Keffa : Keywords Extraction For French Articles

Keffa is a program in Python for extract keywords from French articles in txt format. It uses Python [textblob](https://textblob.readthedocs.io/en/dev/) library.

## Installing and requirements

You need Python >= 2.6 or >= 3.3

You must install textblob and textblob-fr for using Keffa :

```
$ pip install -U textblob
$ pip install -U textblob-fr
```

## How to use

```
usage: keffa.py [-h] -i INPUT -o OUTPUT                                                                                                             
Keffa is a program for extract keywords from French articles in txt format. It uses Python TextBlob library.                                                         
optional arguments:                                                                                                                                                         
  -h, --help                       show this help message and exit                                                                                                                     
  -i INPUT, --input INPUT          Entry folder of text files to be analysed                                                                                                           
  -o OUTPUT, --output OUTPUT       Output folder where extracted keywords will be stored
  ```