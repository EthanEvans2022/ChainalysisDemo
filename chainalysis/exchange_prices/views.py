from django.shortcuts import render
from django.http import HttpResponse
from tools.price_fetcher import fetch_books, calculate_recommendations

# Create your views here.
def home(request):
    context_info = {}
    coins = []
    exchanges = ("coinbasepro", "gemini")
    coins.append(get_coin("BTC", exchanges, count=3))
    coins.append(get_coin("ETH", exchanges, count=3))
    context_info["coins"] = coins
    return render(request,'exchange.html', context=context_info)

#Helper functions (NOT VIEWS)
def get_coin(coin, exchanges, quote="USD", count=5):
    exchange_books = []
    for exchange in exchanges:
        exchange_books.append(fetch_books(exchange, coin, quote, count))
    rec = calculate_recommendations(exchange_books)

    return {"name": coin, "exchanges": exchange_books, "recommendation": rec}

