class RabinKarp:
    def __init__(self, str, substr):
        self.x = 263
        self.p = 10000007
        self.str = str
        self.substr = substr
        self.pows = [pow(self.x, i, self.p) for i in range(len(self.substr))]
        self.ans = []

    def get_start_hash_value(self):
        start_hash = 0
        for i in range(len(self.str) - len(self.substr), len(self.str), 1):
            start_hash += (ord(self.str[i]) * self.pows[i - (len(self.str) - len(self.substr))]) % self.p
        return start_hash % self.p

    def get_hash_pattern(self):
        hash_pattern = 0
        for i in range(len(self.substr)):
            hash_pattern += (ord(self.substr[i]) * self.pows[i]) % self.p
        return hash_pattern % self.p

    def is_match(self, start):
        flag = True
        for j in range(len(self.substr)):
            if self.substr[j] != self.str[start + j]:
                flag = False
                break
        if flag:
            self.ans.append(start)

    def hashing(self):
        hash_prev = self.get_start_hash_value()
        hash_pattern = self.get_hash_pattern()
        if hash_prev == hash_pattern:
            self.is_match(len(self.str) - len(self.substr))
        for i in range(len(self.str) - len(self.substr) - 1, -1, -1):
            flag = True
            hash_current = ((hash_prev - ord(self.str[i + len(self.substr)]) * self.pows[
                len(self.pows) - 1]) * self.x + ord(self.str[i])) % self.p
            if hash_current == hash_pattern:
                self.is_match(i)
            hash_prev = hash_current

    def get_ans(self):
        self.ans.sort()
        return ' '.join(map(str, self.ans))


if __name__ == "__main__":
    pattern = input()
    text = input()
    rk = RabinKarp(text, pattern)
    rk.hashing()
    print(rk.get_ans())
