from django.shortcuts import render
from django.http import HttpResponse
from tools.price_fetcher import get_coin 
from django.template.defaulttags import register

# custom filters
@register.filter
def camel(string):
    return string[0].capitalize() + string[1:]

# Create your views here.
def home(request):
    context_info = {}
    coins = []
    exchanges = ("coinbasepro", "gemini")
    coins.append(get_coin("BTC", exchanges, count=5))
    coins.append(get_coin("ETH", exchanges, count=5))
    context_info["coins"] = coins
    return render(request,'exchange.html', context=context_info)
