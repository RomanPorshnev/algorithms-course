class MinHeap:
    def __init__(self, data):
        self.ans = []
        self.data = data
        self.size = len(data)

    @staticmethod
    def get_left_child(index):
        return 2 * index + 1

    @staticmethod
    def get_right_child(index):
        return 2 * index + 2

    def sift_down(self, index):
        min_index = index
        left_child_index = self.get_left_child(index)
        if left_child_index < self.size and self.data[left_child_index] < self.data[min_index]:
            min_index = left_child_index
        right_child_index = self.get_right_child(index)
        if right_child_index < self.size and self.data[right_child_index] < self.data[min_index]:
            min_index = right_child_index
        if index != min_index:
            self.data[min_index], self.data[index] = self.data[index], self.data[min_index]
            self.sift_down(min_index)

    def solve(self, tasks):
        for task in tasks:
            proc_info = []
            time = self.data[0][0]
            processor = self.data[0][1]
            proc_info.append(processor)
            proc_info.append(time)
            self.ans.append(proc_info)
            self.data[0][0] += task
            self.sift_down(0)

    def get_ans(self):
        return self.ans


if __name__ == "__main__":
    n, m = map(int, input().split())
    tasks = list(map(int, input().split()))
    data = [[0, i] for i in range(n)]
    heap = MinHeap(data)
    heap.solve(tasks)
    ans = heap.get_ans()
    for i in range(len(ans)):
        print(ans[i][0], ans[i][1])
