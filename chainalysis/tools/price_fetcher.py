#!/usr/bin/env python3
import shrimpy
import json
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
public_key="4120ad4bc0a5e079bd1bebdca2d43d531074bb8605ed334a5ab81a5f651469d7"
#TO-DO: GET KEY HERE WHILE ENCRYPTED if have time
secret_key="DUMMY123"
client = shrimpy.ShrimpyApiClient(public_key, secret_key)

def fetch_books(exchange, baseSymbol=None, quoteSymbol=None, limit=5):
    orderbooks =  client.get_orderbooks(exchange, baseSymbol, quoteSymbol, limit)[0]#returns list of dicts
    return filter_raw_books(orderbooks)

def filter_raw_books(raw_books):
    cleaned_books = {}
    cleaned_books["base"] = raw_books["baseSymbol"]
    cleaned_books["quote"] = raw_books["quoteSymbol"]
    cleaned_books["name"] = raw_books["orderBooks"][0]["exchange"]
    books=[]
    books.append({"name": "Asks", "offers": raw_books["orderBooks"][0]["orderBook"]["asks"]})
    books.append({"name": "Bids", "offers": raw_books["orderBooks"][0]["orderBook"]["bids"]})
    cleaned_books["books"] = books
    return cleaned_books

def print_exchanges():
    supported_exchanges = client.get_supported_exchanges()
    for exchange in supported_exchanges:
        print(exchange["exchange"])

def print_book(book):
    print(*book, sep="\n")

def print_tickers(exchange):
    print(client.get_ticker(exchange))
