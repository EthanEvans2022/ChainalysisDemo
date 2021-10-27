#!/usr/bin/env python3
import shrimpy
import json
public_key="4120ad4bc0a5e079bd1bebdca2d43d531074bb8605ed334a5ab81a5f651469d7"
#TO-DO: GET KEY HERE WHILE ENCRYPTED if have time
secret_key="DUMMY123"
client = shrimpy.ShrimpyApiClient(public_key, secret_key)

def fetch_books(exchange, baseSymbol=None, quoteSymbol=None, limit=5):
    orderbooks = client.get_orderbooks(exchange, baseSymbol, quoteSymbol, limit)[0] #returns list of dicts
    asks = orderbooks["orderBooks"][0]["orderBook"]["asks"]
    bids = orderbooks["orderBooks"][0]["orderBook"]["bids"]
    return (bids, asks)

def print_exchanges():
    supported_exchanges = client.get_supported_exchanges()
    for exchange in supported_exchanges:
        print(exchange["exchange"])

def print_book(book):
    print(*book, sep="\n")

def print_tickers(exchange):
    print(client.get_ticker(exchange))
