def coin_change(coins, amount):
    coins.sort(reverse=True)
    result = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
    return len(result)

amount = int(input())
coins = list(map(int, input().split(', ')))
result = coin_change(coins, amount)
print(result)