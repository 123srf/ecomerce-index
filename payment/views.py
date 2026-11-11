from django.shortcuts import render
from shop.context_processors import RATES, SYMBOLS


def _currency_context(request):
    currency = request.session.get('currency', 'USD')
    return {
        'currency': currency,
        'currency_rate': RATES.get(currency, 1),
        'currency_symbol': SYMBOLS.get(currency, '$'),
    }


def checkout(request):
    context = _currency_context(request)
    return render(request, 'checkout.html', context)


def cart(request):
    context = _currency_context(request)
    return render(request, 'cart.html', context)
