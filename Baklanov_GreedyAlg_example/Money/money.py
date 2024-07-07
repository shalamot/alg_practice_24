def coin_change(coins, amount):
    coins.sort(reverse=True)
    result = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
    return len(result)

if __name__ == "__main__":
    amount = int(input())
    coins = list(map(int, input().split(', ')))
    result = coin_change(coins, amount)
    print(result)