a = ["hey", 'Bull cross section', 'SELL NOTE', "BUY NOW", 'BEAR', 'BULL', 'now sell', '']

# print(  int(''.join([x for x in a if x.isdigit()]))  )

def rank_title(title):
    if 'buy' in title.lower() or 'bull' in title.lower():
        return 0
    if 'sell' in title.lower() or 'bear' in title.lower():
        return 1
    else:
        return 2

result = sorted(a, key=lambda x: (is_buy(x), x))

print(result)