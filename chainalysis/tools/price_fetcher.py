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
    '''
    cleaned_books = {}
    cleaned_books["base"] = raw_books["baseSymbol"]
    cleaned_books["quote"] = raw_books["quoteSymbol"]
    cleaned_books["name"] = raw_books["orderBooks"][0]["exchange"]
    books=[]
    books.append({"name": "Asks", "offers": list(map(formatted_offers, raw_books["orderBooks"][0]["orderBook"]["asks"]))})
    books.append({"name": "Bids", "offers": list(map(formatted_offers, raw_books["orderBooks"][0]["orderBook"]["bids"]))})
    cleaned_books["books"] = books
    '''
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


def print_exchanges():
    supported_exchanges = client.get_supported_exchanges()
    for exchange in supported_exchanges:
        print(exchange["exchange"])

def print_book(book):
    print(*book, sep="\n")

def print_tickers(exchange):
    print(client.get_ticker(exchange))
