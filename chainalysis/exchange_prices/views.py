from django.shortcuts import render
from django.http import HttpResponse
from tools.price_fetcher import fetch_books, calculate_recommendations
from django.template.defaulttags import register
@register.filter
def camel(string):
    return string
    #IMPLEMENT
# Create your views here.
def home(request):
    context_info = {}
    coins = []
    exchanges = ("coinbasepro", "gemini")
    coins.append(get_coin("BTC", exchanges, count=1))
    coins.append(get_coin("ETH", exchanges, count=1))
    context_info["coins"] = coins
    return render(request,'exchange.html', context=context_info)

#Helper functions (NOT VIEWS)
def get_coin(coin, exchanges, quote="USD", count=5):
    exchange_books = []
    asks, bids = {}, {}
    asks["exchanges"], bids["exchanges"] = [], []
    asks["name"] = "asks"
    bids["name"] = "bids"
    for exchange in exchanges:
        #exchange_books.append(fetch_books(exchange, coin, quote, count))
        exc_asks, exc_bids = fetch_books(exchange, coin, quote, count)
        asks["exchanges"].append(exc_asks)
        bids["exchanges"].append(exc_bids)
    asks["recommendation"] = calculate_recommendations(asks["exchanges"], minimize=True)
    bids["recommendation"] = calculate_recommendations(bids["exchanges"], minimize=False) #change to be added to asks + bids dicts

    #return {"name": coin, "exchanges": exchange_books, "recommendation": rec}
    return {"name": coin, "books": (asks, bids)}


