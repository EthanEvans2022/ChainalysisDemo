from django.shortcuts import render
from django.http import HttpResponse
from tools.price_fetcher import fetch_books

# Create your views here.
def home(request):
    context_info = {}
    coins = []
    exchanges = ("coinbasepro", "gemini")
    coins.append(get_coin("BTC", exchanges))
    coins.append(get_coin("ETH", exchanges))
    context_info["coins"] = coins
    return render(request,'exchange.html', context=context_info)

#Helper functions (NOT VIEWS)
def get_coin(coin, exchanges, quote="USD", count=5):
    books = []
    for exchange in exchanges:
        books.append(fetch_books(exchange, coin, quote, count))
    return {"name": coin, "exchanges": books}

