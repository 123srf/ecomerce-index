RATES = {
    'USD': 1,
    'EUR': 0.92,
    'GBP': 0.79,
    'CAD': 1.36,
}

SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'CAD': 'C$',
}


def currency(request):
    currency = request.session.get('currency', 'USD')

    return {
        'currency': currency,
        'currency_rate': RATES.get(currency, 1),
        'currency_symbol': SYMBOLS.get(currency, '$')
    }
