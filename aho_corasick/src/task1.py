import queue

'''
Данная структура содержит информацию о каждом узле бора: суффиксную ссылку на другой узел, 
является ли данный узел бора образцом, какой узел является родителем данного, 
быстрая суффиксная ссылка (суффиксная ссылка на ближайший терминальный узел), список потомков данного узла.
'''


class NodeInfo:
    def __init__(self, suffix_link, is_terminal, parent):
        self.suffix_link = suffix_link
        self.is_terminal = is_terminal
        self.parent = parent
        self.fast_suffix_link = None
        self.children_names = []


'''
Класс, содержащий инструменты для решения поставленной задачи.
'''


class AhoCorasick:

    '''
    Конструктор для инициализация начальных данных.
    Входные данные: текст, список образцов, символ, который гарантированно не содержится в образцах.
    '''

    def __init__(self, input_text, input_patterns, null_symbol):
        self.__null_symbol = null_symbol
        self.__text = input_text
        self.__patterns = input_patterns
        self.__trie = {self.__null_symbol: NodeInfo(None, False, self.__null_symbol)}
        self.__answer = {}

    '''
    Данный метод запускает решение задачи: построение бора, создание суффиксных ссылок, 
    создание быстрых суффиксных ссылок, запуск автомата для получения предварительных данных, 
    обработка предварительных данных -> получение ответа на задачу, печать ответа на экран.
    '''

    def run(self):
        self.__build_trie()
        self.__make_suffix_links()
        self.__make_fast_suffix_links()
        self.__search_for_occurrences()
        self.__handle_answer()
        self.__print_answer()

    '''
    Данный метод строит бор по полученным образцам.
    '''

    def __build_trie(self):
        for pattern in self.__patterns:
            node_name = ''
            for i in range(len(pattern)):
                node_name += pattern[i]
                if node_name not in self.__trie:
                    node_info = NodeInfo(self.__null_symbol, i == len(pattern) - 1, node_name[:len(node_name) - 1])
                    self.__trie[node_name[:len(node_name) - 1]].children_names.append(node_name)
                    self.__trie[node_name] = node_info
                elif node_name in self.__trie and i == len(pattern) - 1:
                    self.__trie[node_name].is_terminal = True

    '''
    Данный метод создает суффиксные ссылки для каждого узла бора.
    Алгоритм представляет собой "ленивую" динамику, 
    то есть новые суффиксные ссылки создаются на основе уже существующих.
    '''

    def __make_suffix_links(self):
        nodes_names = queue.Queue()
        nodes_names.put(self.__null_symbol)
        while not nodes_names.empty():
            node_name = nodes_names.get()
            transit_node_name = self.__trie[self.__trie[node_name].parent].suffix_link
            edge_weight = node_name[len(node_name) - 1]
            suffix_link_was_found = False
            while transit_node_name is not None:
                children = self.__trie[transit_node_name].children_names
                for child in children:
                    if child[len(child) - 1] == edge_weight:
                        self.__trie[node_name].suffix_link = child
                        suffix_link_was_found = True
                        break
                if suffix_link_was_found:
                    break
                else:
                    transit_node_name = self.__trie[transit_node_name].suffix_link
            children_names = self.__trie[node_name].children_names
            for child_name in children_names:
                nodes_names.put(child_name)

    '''
    Данный метод создает быстрые суффиксные ссылки на основе уже созданных суффиксных ссылок.
    Алгоритм представляет собой "ленивую" динамику, 
    то есть новые быстрые суффиксные ссылки создаются на основе уже существующих или на основании того, 
    что сейчас указатель автомата находится на терминальном узле.
    '''

    def __make_fast_suffix_links(self):
        nodes_names = queue.Queue()
        nodes_names.put(self.__null_symbol)
        while not nodes_names.empty():
            node_name = nodes_names.get()
            transit_node_name = self.__trie[node_name].suffix_link
            while transit_node_name is not None:
                if self.__trie[transit_node_name].is_terminal:
                    self.__trie[node_name].fast_suffix_link = transit_node_name
                    break
                elif self.__trie[transit_node_name].fast_suffix_link is not None:
                    self.__trie[node_name].fast_suffix_link = self.__trie[transit_node_name].fast_suffix_link
                    break
                transit_node_name = self.__trie[transit_node_name].suffix_link
            children_names = self.__trie[node_name].children_names
            for child_name in children_names:
                nodes_names.put(child_name)

    '''
    Данный метод предназначен для получения предварительных данных, 
    которые затем можно интерпретировать как ответ на задачу.
    Автомат двигается по символам текста и узлам бора. Если есть возможность перейти в новое состояние по потомку узла, 
    то автомат перейдёт к данному потомку, иначе произойдёт переход по суффиксной ссылке 
    и там установится наличие возможности, оговоренной выше. Если текущего символа нет в потомке и для данного узла нет 
    суффиксной ссылки, значит, автомат пропускает данный символ текста и переходит к следующему.
    Если автомат оказался в терминальном узле, значит в тексте был найден один из образцов и эти данные нужно 
    зафиксировать для дальнейшей обработки и получения ответа на исходную задачу.
    '''

    def __search_for_occurrences(self):
        current_node_name = self.__null_symbol
        i = 0
        while i < len(self.__text):
            children_names = self.__trie[current_node_name].children_names
            child_was_found = False
            for child_name in children_names:
                if child_name[-1] == self.__text[i]:
                    current_node_name += child_name[-1]
                    child_was_found = True
                    i += 1
                    break
            if not child_was_found:
                if self.__trie[current_node_name].suffix_link is not None:
                    current_node_name = self.__trie[current_node_name].suffix_link
                else:
                    i += 1
                continue
            if not self.__trie[current_node_name].is_terminal and self.__trie[
                current_node_name].fast_suffix_link is None:
                continue
            pattern_node_name = current_node_name
            while pattern_node_name is not None:
                if self.__trie[pattern_node_name].is_terminal:
                    if i - len(pattern_node_name) + 2 not in self.__answer:
                        self.__answer[i - len(pattern_node_name) + 2] = [self.__patterns[pattern_node_name]]
                    else:
                        self.__answer[i - len(pattern_node_name) + 2].append(self.__patterns[pattern_node_name])
                pattern_node_name = self.__trie[pattern_node_name].fast_suffix_link

    '''
    Данный метод предназначен для обработки предварительных данных, 
    которые после обработки и являются ответом на исходную задачу.
    Предварительные данные содержатся в словаре self.__answer, где ключ -- это образец, 
    а значения -- списки позиций вхождений данного образца в текст. В роли значений выступают списки, 
    а не список позиций, так как входные данные не гарантируют того, что каждый образец входит единожды. 
    Если алгоритм в методе __search_for_occurrences(self) находит вхождения некоторого образца, 
    то к ключу данного образца добавляется список позиций вхождений данного образца в текст. 
    Если в будущем данный автомат снова попадёт на данный образец, к значениям данного ключа добавится ещё один список 
    позиций вхождений данного образца в текст. Данный метод раскрывает все эти списки, преобразуя в один. Затем 
    происходит сортировка ключей словаря и значений каждого ключа. Полученный словарь и является ответом на задачу.
    '''

    def __handle_answer(self):
        for position in self.__answer:
            numbers_of_patterns = []
            for elem in self.__answer[position]:
                for number_of_pattern in elem:
                    numbers_of_patterns.append(number_of_pattern)
            self.__answer[position] = numbers_of_patterns
        self.__answer = dict(sorted(self.__answer.items(), key=lambda x: x[0]))
        for position in self.__answer:
            self.__answer[position].sort()

    '''
    Данный метод предназначен для печати ответа на экран.
    '''

    def __print_answer(self):
        for position in self.__answer:
            for number_of_pattern in self.__answer[position]:
                print(position, number_of_pattern)


'''
Данный класс предназначен для считывания начальных данных и их получения.
'''


class InputData:
    '''
    Данный конструктор инициализирует символ null_symbol, который гарнтирвоанно не будет встречаться ни в образцах,
    ни в тексте.
    '''

    def __init__(self, null_symbol):
        self.__patterns = {}
        self.__text = ''
        self.__null_symbol = null_symbol

    '''
    Данный метод предназначен для считывания текста, количества образцов и самих образцов непосредственно. 
    К началу строки каждого образца добавляется специльный символ null_symbol, 
    который нужен для корректного построения бора.
    '''

    def read_text_and_patterns(self):
        self.__patterns = {}
        self.__text = input()
        number_of_patterns = int(input())
        for i in range(number_of_patterns):
            pattern = self.__null_symbol + input()
            if pattern not in self.__patterns:
                self.__patterns[pattern] = [i + 1]
            else:
                self.__patterns[pattern].append(i + 1)

    '''
    Данный метод предназначен для получения текста.
    '''

    def get_text(self):
        return self.__text

    '''
    Данный метод предназначен для получения списка образцов.
    '''

    def get_patterns(self):
        return self.__patterns


if __name__ == "__main__":
    input_data_reader = InputData(' ')
    input_data_reader.read_text_and_patterns()
    aho_corasick = AhoCorasick(input_data_reader.get_text(), input_data_reader.get_patterns(), ' ')
    aho_corasick.run()
