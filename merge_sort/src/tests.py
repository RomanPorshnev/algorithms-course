from main import merge_sort


def test_1():
    matrix_data = [[0, 32], [1, 11], [2, 3]]
    numb_matrix = []
    merge_sort(matrix_data, numb_matrix)
    ans = ''
    for i in range(len(matrix_data)):
        ans += ' ' + str(matrix_data[i][0])
    ans = ans[1:]
    numb_matrix.append(ans)
    assert numb_matrix == ['2 1', '2 1 0', '2 1 0']


def test_2():
    matrix_data = [[0, 100], [1, 20], [2, 1], [3, -1000], [4, -1001], [5, 1111]]
    numb_matrix = []
    merge_sort(matrix_data, numb_matrix)
    ans = ''
    for i in range(len(matrix_data)):
        ans += ' ' + str(matrix_data[i][0])
    ans = ans[1:]
    numb_matrix.append(ans)
    assert numb_matrix == ['2 1', '2 1 0', '4 5', '4 3 5', '4 3 2 1 0 5', '4 3 2 1 0 5']


def test_3():
    matrix_data = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]
    numb_matrix = []
    merge_sort(matrix_data, numb_matrix)
    ans = ''
    for i in range(len(matrix_data)):
        ans += ' ' + str(matrix_data[i][0])
    ans = ans[1:]
    numb_matrix.append(ans)
    assert numb_matrix == ['0 1', '3 4', '2 3 4', '0 1 2 3 4', '0 1 2 3 4']


def test_4():
    matrix_data = [[0, 1]]
    numb_matrix = []
    merge_sort(matrix_data, numb_matrix)
    ans = ''
    for i in range(len(matrix_data)):
        ans += ' ' + str(matrix_data[i][0])
    ans = ans[1:]
    numb_matrix.append(ans)
    assert numb_matrix == ['0']


def test_5():
    matrix_data = [[0, 10], [1, 11], [2, 15], [3, 25], [4, 50], [5, 100]]
    numb_matrix = []
    merge_sort(matrix_data, numb_matrix)
    ans = ''
    for i in range(len(matrix_data)):
        ans += ' ' + str(matrix_data[i][0])
    ans = ans[1:]
    numb_matrix.append(ans)
    assert numb_matrix == ['1 2', '0 1 2', '4 5', '3 4 5', '0 1 2 3 4 5', '0 1 2 3 4 5']
