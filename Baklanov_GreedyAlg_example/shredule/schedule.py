def shredule(tasks):
    sorted_tasks = sorted(tasks, key=lambda x: x[1])
    res = []
    begin = 8
    current_end = begin
    end = 17
    for task in sorted_tasks:
        if not((begin <= task[0] < end) and (begin < task[1] <= end)):
            continue
        if task[0] >= current_end:
            res.append(task)
            current_end = task[1]
    return len(res)

if __name__ == "__main__":
    n = int(input())
    tasks = []
    for i in range(n):
        tasks.append(list(map(int, input().split(', '))))
    print(shredule(tasks))