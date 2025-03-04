def merge_sort(arr, numb_matrix):
    if len(arr) == 1 or len(arr) == 0:
        return arr
    L = merge_sort(arr[:len(arr) // 2], numb_matrix)
    R = merge_sort(arr[len(arr) // 2:], numb_matrix)
    n = m = k = 0
    C = [[0, 0]] * (len(L) + len(R))
    while n < len(L) and m < len(R):
        data = []
        if L[n][1] <= R[m][1]:
            data.append(L[n][0])
            data.append(L[n][1])
            C[k] = data
            n += 1
        else:
            data.append(R[m][0])
            data.append(R[m][1])
            C[k] = data
            m += 1
        k += 1
    while n < len(L):
        data = []
        data.append(L[n][0])
        data.append(L[n][1])
        C[k] = data
        n += 1
        k += 1
    while m < len(R):
        data = []
        data.append(R[m][0])
        data.append(R[m][1])
        C[k] = data
        m += 1
        k += 1
    ans = ''
    for i in range(len(arr)):
        ans += ' ' + str(C[i][0])
        arr[i] = C[i]
    ans = ans[1:]
    numb_matrix.append(ans)
    return arr


def sum(matrix):
    sum = 0
    for i in range(len(matrix)):
        sum += matrix[i][i]
    return sum


def ans(matrix_data):
    numb_matrix = []
    matrix_data = merge_sort(matrix_data, numb_matrix)
    ans = ''
    for i in range(len(matrix_data)):
        ans += ' ' + str(matrix_data[i][0])
    ans = ans[1:]
    numb_matrix.append(ans)
    return numb_matrix


if __name__ == '__main__':
    n = int(input())
    matrix_data = []
    for i in range(n):
        matrix = []
        size_matrix = int(input())
        for j in range(size_matrix):
            row = list(map(int, input().split()))
            matrix.append(row)
        data = []
        data.append(i)
        data.append(sum(matrix))
        matrix_data.append(data)
    numb_matrix = ans(matrix_data)
    for i in range(len(numb_matrix)):
        print(numb_matrix[i])
