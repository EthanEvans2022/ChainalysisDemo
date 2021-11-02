from django.shortcuts import render
from django.http import HttpResponse
from tools.price_fetcher import fetch_books, calculate_recommendations

# Create your views here.
def home(request):
    context_info = {}
    coins = []
    exchanges = ("coinbasepro", "gemini")
    print("getting BTC")
    coins.append(get_coin("BTC", exchanges, count=3))
    print("getting ETH")
    coins.append(get_coin("ETH", exchanges, count=3))
    print("Got all coins")
    context_info["coins"] = coins
    return render(request,'exchange.html', context=context_info)

#Helper functions (NOT VIEWS)
def get_coin(coin, exchanges, quote="USD", count=5):
    exchange_books = []
    for exchange in exchanges:
        print("foo 1")
        exchange_books.append(fetch_books(exchange, coin, quote, count))
    buy_rec, sell_rec = calculate_recommendations(exchange_books)
    return {"name": coin, "exchanges": exchange_books, "recommendation": (buy_rec, sell_rec)}

