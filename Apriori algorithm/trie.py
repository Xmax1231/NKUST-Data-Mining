class Node:
    __slots__ = ['n', 'child', 'child_n', 'extend_i']
    def __init__(self, n):
        self.n = n
        self.child = []
        self.child_n = []
        self.extend_i = None

    def is_leaf(self):
        return True if len(self.child) == 0 else False
    
    def get_index(self, n):
        # for i, x in enumerate(self.child):
        #     if x.n == n:
        #         return i
        # return -1
        try:
            return self.child_n.index(n)
        except ValueError:
            return -1
    
    def add_child(self, n):
        self.child.append(Node(n))
        self.child_n.append(n)
    
    def __del__(self):
        for c in self.child:
            del c
        del self

    def __repr__(self):
        return '{}'.format(self.n)

class Trie:
    __slots__ = ['root']
    def __init__(self):
        self.root = Node(n='root')

    def insert(self, items, index):
        temp_root = self.root
        for d in items:
            child_index = temp_root.get_index(d)
            if child_index == -1:
                temp_root.add_child(d)
            temp_root = temp_root.child[child_index]
        temp_root.extend_i = index

    def __del__(self):
        del self.root
        del self

if __name__ == "__main__":
    t = Trie()
    t.insert([5])
    t.insert([6])
    t.insert([5, 6])

    print(t.root.child)
    print(t.root.child[0].child)