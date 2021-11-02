#!/usr/bin/env python3
import shrimpy
import json
import math
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
public_key="4120ad4bc0a5e079bd1bebdca2d43d531074bb8605ed334a5ab81a5f651469d7"
#TO-DO: GET KEY HERE WHILE ENCRYPTED if have time
secret_key="DUMMY123"
client = shrimpy.ShrimpyApiClient(public_key, secret_key)

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

def fetch_books(exchange, baseSymbol=None, quoteSymbol=None, limit=5):
    print("fetching book")
    orderbooks =  client.get_orderbooks(exchange, baseSymbol, quoteSymbol, limit)[0]#returns list of dicts
    print("orderbooks:")
    print(orderbooks)
    return filter_raw_books(orderbooks)

def calculate_recommendations(exchanges):
    '''
    have list of exchanges
        name
        books[]
            name
            offers[]
                price: str
                quantity: str

    track best buy/sell price at each exchange
    loop through all exchanges and get the best
    '''
    print("finding recommendation")
    return recur_recommendation(exchanges)

def recur_recommendation(exchanges):
    print("help")
    best_ask = (math.inf, "ERROR")
    best_bid = (-math.inf, "ERROR")
    if len(exchanges) == 1:
        name = exchanges[0]["name"]
        ask = exchanges[0]["books"][0]["offers"][0]
        bid = exchanges[0]["books"][1]["offers"][0]
        return (ask, name), (bid, name)

    midpoint = int(len(exchanges)/2)
    left = exchanges[:midpoint]
    right = exchanges[midpoint:]
    best_ask_left, best_bid_left = recur_recommendation(left)
    best_ask_right, best_bid_right = recur_recommendation(right)

    best_ask = best_ask_left if best_ask_left[0]["price"] == min(best_ask_left[0]["price"], best_ask_right[0]["price"]) else best_ask_right
    best_bid = best_bid_right if best_bid_left[0]["price"] == max(best_bid_left[0]["price"], best_bid_right[0]["price"]) else best_bid_right
    return best_ask, best_bid


def print_exchanges():
    supported_exchanges = client.get_supported_exchanges()
    for exchange in supported_exchanges:
        print(exchange["exchange"])

def print_book(book):
    print(*book, sep="\n")

def print_tickers(exchange):
    print(client.get_ticker(exchange))
