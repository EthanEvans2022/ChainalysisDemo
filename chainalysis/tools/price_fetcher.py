import shrimpy
import json
import math
from django.template.defaulttags import register
from secrets.auth import get_client


def formatted_offers(offer):
    price = float(offer["price"])
    quantity = float(offer["quantity"])
    return {"price": offer["price"], "quantity": offer["quantity"], "total": round(price * quantity, 2)}

def filter_raw_books(raw_books):
    exchange = raw_books["orderBooks"][0]["exchange"]
    asks = list(map(formatted_offers, raw_books["orderBooks"][0]["orderBook"]["asks"]))
    bids = list(map(formatted_offers, raw_books["orderBooks"][0]["orderBook"]["bids"]))
    return {"name": exchange, "offers": asks}, {"name": exchange, "offers": bids}

def fetch_books(exchange, baseSymbol=None, quoteSymbol=None, limit=5):
    try:
        client = get_client()
        orderbooks =  client.get_orderbooks(exchange, baseSymbol, quoteSymbol, limit)[0]#returns list of dicts
    except Exception as err:
        print(err)
    return filter_raw_books(orderbooks)

def calculate_recommendations(exchanges, minimize):
    return  recur_recommendation(exchanges, minimize)

def recur_recommendation(exchanges, minimize):
    if len(exchanges) == 1:
        name = exchanges[0]["name"]
        offer = exchanges[0]["offers"][0]
        return {"offer": offer, "exchange": name}

    midpoint = int(len(exchanges)/2)
    left = exchanges[:midpoint]
    right = exchanges[midpoint:]
    best_left = recur_recommendation(left, minimize)
    best_right = recur_recommendation(right, minimize)

    if minimize:
        best_offer = best_left if best_left["offer"]["price"] == min(best_left["offer"]["price"], best_right["offer"]["price"]) else best_right
    else:
        best_offer = best_left if best_left["offer"]["price"] == max(best_left["offer"]["price"], best_right["offer"]["price"]) else best_right

    return  best_offer

def get_coin(coin, exchanges, quote="USD", count=5):
    exchange_books = []
    asks, bids = {}, {}
    asks["exchanges"], bids["exchanges"] = [], []
    asks["name"] = "asks"
    bids["name"] = "bids"
    for exchange in exchanges:
        exc_asks, exc_bids = fetch_books(exchange, coin, quote, count)
        asks["exchanges"].append(exc_asks)
        bids["exchanges"].append(exc_bids)
    asks["recommendation"] = calculate_recommendations(asks["exchanges"], minimize=True)
    bids["recommendation"] = calculate_recommendations(bids["exchanges"], minimize=False) #change to be added to asks + bids dicts

    return {"name": coin, "books": (asks, bids)}
