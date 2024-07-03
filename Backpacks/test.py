import random
from backpacks import maximize_loot

def generate(key = 0): #Функция генерации тестов, по умолчанию предслагает заранее написанные тесты, при подставновке ненулевого аргумента генерирует рандомные страшные тесты
    if key == 0:
        dataset = ['30\n5\n3, 10\n5, 15\n7, 20\n8, 25\n10, 30', '40\n6\n4, 12\n6, 20\n9, 28\n12, 35\n15, 40\n18, 45', '50\n10\n2, 10\n4, 15\n6, 20\n8, 25\n10, 30\n12, 35\n14, 40\n16, 45\n18, 50\n20, 55\n22, 60\n24, 65\n26, 70\n28, 75\n30, 80\n32, 85\n34, 90\n36, 95\n38, 100\n40, 105\n42, 110\n44, 115\n46, 120\n48, 125\n50, 130\n52, 135\n54, 140\n56, 145\n58, 150\n60, 155']
    else:
        dataset = []
        for i in range(3):
            capacity = random.randint(200, 500)
            num_items = random.randint(3, 100)
            items = []
            for _ in range(num_items):
                weight = random.randint(1, 50)
                value = random.randint(10, 140)
                items.append((weight, value))
            dataset_i = f"{capacity}\n{num_items}\n"
            for weight, value in items:
                dataset_i += f"{weight}, {value}\n"
            dataset.append(dataset_i)
    return dataset




#
def maximize_loot(dataset):
    lines = dataset.split('\n')
    capacity, num_items = int(lines[0]), int(lines[1])
    items = []
    for line in lines[2:]:
        if line != '':
            print(line)
            weight, value = map(int, line.split(', '))
            items.append((weight, value))
    items_with_ratio = [(item[0], item[1], item[1] / item[0]) for item in items]
    items_with_ratio.sort(key=lambda x: x[2], reverse=True)
    loot = []
    current_weight = 0
    current_value = 0

    for weight, value, ratio in items_with_ratio:
        if current_weight + weight <= capacity:
            loot.append((weight, value))
            current_weight += weight
            current_value += value

    return current_weight, current_value

tests = generate()
for test in tests:
    res_weight, res_value = maximize_loot(test)
    print(res_weight, res_value)
