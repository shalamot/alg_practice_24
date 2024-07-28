def generate():
    dataset = ['63\n1, 5, 10, 25', '255\n1, 6, 12, 20, 34, 22, 63, 5, 7', '666666\n1, 5, 7 9, 19, 1, 17, 20, 21, 56, 112']
    return dataset



def coin_change(dataset):
    data = dataset.split('\n')
    amount = int(data[0])
    coins = list(map(int, data[1].split(', ')))
    coins.sort(reverse=True)
    result = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
    return len(result)

tests = generate()

res = coin_change(tests[1])
print(res)