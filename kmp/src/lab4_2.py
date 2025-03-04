# Данная функция вычисляет префикс-функцию для строки, переданной на вход.
# Входные данные: строка, для которой нужно вычислить префикс-функцию.
# Выходные данные: префикс-функция для строки, переданной на вход.
def compute_prefix_function(pattern):
    pattern_length = len(pattern)
    prefix_function = [0] * pattern_length
    j = 0
    for i in range(1, pattern_length):
        while j > 0 and pattern[i] != pattern[j]:
            j = prefix_function[j - 1]
        if pattern[j] == pattern[i]:
            j += 1
        prefix_function[i] = j
    return prefix_function


# Данный метод предназначен для поиска индекса начала строки pattern в text
# при том, что text -- это удвоенная первая введённая строка, а pattern -- вторая
# введённая строка.
# Входные данные: первая введённая строка * 2, вторая строка.
# Выходные данные: индекс начала второй введённой строки в первой, умноженной на 2.
def find_shift_position(text, pattern):
    pattern_length = len(pattern)
    text_length = len(text)
    shift_position = -1
    j = 0
    if pattern_length == text_length // 2:
        prefix_function = compute_prefix_function(pattern)
        for i in range(text_length):
            while j > 0 and pattern[j] != text[i]:
                j = prefix_function[j - 1]
            if pattern[j] == text[i]:
                j += 1
            if j == pattern_length:
                shift_position = i - pattern_length + 1
                break
    return shift_position


# Данный метод предназначен для вывода индекса начала
# второй введённой строки в первой, умноженной на 2.
# Входные данные: индекс начала второй введённой строки в первой.
def print_shift_position(shift_position):
    print(shift_position)


# Данный метод предназначен для ввода и получения первой и второй строки.
# Выходные данные: считанные строки
def get_read_text_and_pattern():
    text_input = input()
    pattern_input = input()
    return text_input * 2, pattern_input


# Данный метод запускает логику решения задачи: считывание строк,
# поиск решения, вывод решения.
def run():
    text, pattern = get_read_text_and_pattern()
    shift_position = find_shift_position(text, pattern)
    print_shift_position(shift_position)


if __name__ == "__main__":
    run()
