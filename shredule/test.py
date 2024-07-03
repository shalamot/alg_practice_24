def generate():
    dataset = ['7\n8, 11\n12, 14\n8, 13\n13, 15\n15, 17\n15, 16\n16, 17', '15\n11, 13\n12, 13\n14, 16\n16, 17\n10, 16\n14, 15\n17, 20\n8, 20\n1, 12\n9, 12\n8, 10\n10, 12\n13, 15\n15, 16\n16, 17', '50\n11, 13\n12, 13\n14, 16\n16, 17\n10, 16\n14, 15\n17, 20\n8, 20\n1, 12\n9, 12\n8, 10\n10, 12\n13, 15\n15, 16\n16, 17\n8, 9\n9, 11\n10, 11\n11, 12\n12, 14\n13, 14\n14, 15\n15, 17\n8, 11\n9, 10\n10, 14\n11, 15\n12, 16\n13, 17\n8, 12\n9, 13\n10, 15\n11, 16\n12, 17\n8, 13\n9, 14\n10, 16\n11, 17\n8, 14\n9, 15\n10, 17\n8, 15\n9, 16\n8, 16\n9, 17\n8, 17\n10, 13\n11, 14\n12, 15\n13, 16'
]
    return dataset




def shredule(dataset):
    lines = dataset.split('\n')
    counts = int(lines[0])
    tasks = []
    for line in lines[1:]:
        tasks.append(list(map(int, line.split(', '))))
    sorted_tasks = sorted(tasks, key=lambda x: x[1])
    res = []
    begin = 8
    end = 17
    for task in sorted_tasks:
        if (task[1] > end) or (task[0] >= end):
            continue
        if task[0] >= begin:
            res.append(task)
            begin = task[1]
    return len(res)

tests = generate()

res = shredule(tests[0])
print(res)