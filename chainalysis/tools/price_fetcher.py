#!/usr/bin/env python3
import shrimpy #TODO: see if i can remove this now (probably not)
import json
import math
from django.template.defaulttags import register
from secrets.auth import get_client

#TODO: remove this filter
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def formatted_offers(offer):
    price = float(offer["price"])
    quantity = float(offer["quantity"])
    return {"price": offer["price"], "quantity": offer["quantity"], "total": round(price * quantity, 2)}

def filter_raw_books(raw_books):
    cleaned_books = {}
    cleaned_books["base"] = raw_books["baseSymbol"]
    cleaned_books["quote"] = raw_books["quoteSymbol"]
    cleaned_books["name"] = raw_books["orderBooks"][0]["exchange"]
    books=[]
    books.append({"name": "Asks", "offers": list(map(formatted_offers, raw_books["orderBooks"][0]["orderBook"]["asks"]))})
    books.append({"name": "Bids", "offers": list(map(formatted_offers, raw_books["orderBooks"][0]["orderBook"]["bids"]))})
    cleaned_books["books"] = books
    return cleaned_books

def fetch_books(exchange, baseSymbol=None, quoteSymbol=None, limit=5):
    try:
        client = get_client()
        orderbooks =  client.get_orderbooks(exchange, baseSymbol, quoteSymbol, limit)[0]#returns list of dicts
    except Exception as err:
        print(err)
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
    best_ask, best_bid = recur_recommendation(exchanges)
    return {"best_ask": best_ask, "best_bid": best_bid}

def recur_recommendation(exchanges):
    best_ask = (math.inf, "ERROR")
    best_bid = (-math.inf, "ERROR")
    if len(exchanges) == 1:
        name = exchanges[0]["name"]
        ask = exchanges[0]["books"][0]["offers"][0]
        bid = exchanges[0]["books"][1]["offers"][0]
        return {"offer": ask, "exchange": name}, {"offer": bid, "exchange": name}

    midpoint = int(len(exchanges)/2)
    left = exchanges[:midpoint]
    right = exchanges[midpoint:]
    best_ask_left, best_bid_left = recur_recommendation(left)
    best_ask_right, best_bid_right = recur_recommendation(right)

    best_ask = best_ask_left if best_ask_left["offer"]["price"] == min(best_ask_left["offer"]["price"], best_ask_right["offer"]["price"]) else best_ask_right
    best_bid = best_bid_left if best_bid_left["offer"]["price"] == max(best_bid_left["offer"]["price"], best_bid_right["offer"]["price"]) else best_bid_right
    return  best_ask, best_bid


def print_exchanges():
    supported_exchanges = client.get_supported_exchanges()
    for exchange in supported_exchanges:
        print(exchange["exchange"])

def print_book(book):
    print(*book, sep="\n")

def print_tickers(exchange):
    print(client.get_ticker(exchange))
