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


# Данная функция предназначена для поиска индексов, начиная с которых
# строка pattern входит в text.
# Входные данные: текст и образец.
# Выходные данные: индексы, начиная с которых pattern входит в text.
def kmp_matcher(text, pattern):
    pattern_length = len(pattern)
    text_length = len(text)
    positions_of_occurrences = []
    j = 0
    prefix_function = compute_prefix_function(pattern)
    for i in range(text_length):
        while j > 0 and pattern[j] != text[i]:
            j = prefix_function[j - 1]
        if pattern[j] == text[i]:
            j += 1
        if j == pattern_length:
            positions_of_occurrences.append(str(i - pattern_length + 1))
            j = prefix_function[j - 1]
    return positions_of_occurrences


# Данная функция предназначена для вывода индексов,
# начиная с которых образец входит в текст.
# Входные данные: индексы, начиная с которых образец входит в текст.
def print_positions_of_occurrences(positions_of_occurrences):
    if len(positions_of_occurrences) != 0:
        print(','.join(positions_of_occurrences))
    else:
        print(-1)


# Данная функция предназначена для ввода и получения образца и текста.
# Выходные данные: считанные строки
def get_read_text_and_pattern():
    pattern_input = input()
    text_input = input()
    return text_input, pattern_input


# Данная функция запускает логику решения задачи: считывание образца и текста,
# поиск решения, вывод решения.
def run():
    text, pattern = get_read_text_and_pattern()
    positions_of_occurrences = kmp_matcher(text, pattern)
    print_positions_of_occurrences(positions_of_occurrences)


if __name__ == "__main__":
    run()
