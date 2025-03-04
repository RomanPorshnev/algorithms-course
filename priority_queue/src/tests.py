from main import MinHeap


def test_1():
    n = 2
    tasks = [100, 1]
    data = [[0, i] for i in range(n)]
    heap = MinHeap(data)
    heap.solve(tasks)
    assert heap.get_ans() == [[0, 0], [1, 0]]


def test_2():
    n = 5
    tasks = [0, 0, 0, 0, 0, 0, 0, 0]
    data = [[0, i] for i in range(n)]
    heap = MinHeap(data)
    heap.solve(tasks)
    assert heap.get_ans() == [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]


def test_3():
    n = 1
    tasks = [10]
    data = [[0, i] for i in range(n)]
    heap = MinHeap(data)
    heap.solve(tasks)
    assert heap.get_ans() == [[0, 0]]


def test_4():
    n = 2
    tasks = [2, 2, 2, 2, 2]
    data = [[0, i] for i in range(n)]
    heap = MinHeap(data)
    heap.solve(tasks)
    assert heap.get_ans() == [[0, 0], [1, 0], [0, 2], [1, 2], [0, 4]]


def test_5():
    n = 5
    tasks = [4, 9, 4, 4, 8, 5, 7, 3, 3, 6]
    data = [[0, i] for i in range(n)]
    heap = MinHeap(data)
    heap.solve(tasks)
    assert heap.get_ans() == [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [0, 4], [2, 4], [3, 4], [3, 7], [4, 8]]
