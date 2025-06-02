class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.values = []  # 叶子节点存储值，内部节点存储子节点

class BPlusTree:
    def __init__(self, t=3):
        self.root = BPlusTreeNode(leaf=True)
        self.t = t  # 阶数，最小度数

    def search(self, key, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if node.leaf:
            if i < len(node.keys) and node.keys[i] == key:
                return node.values[i]
            return None
        else:
            return self.search(key, node.values[i])

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BPlusTreeNode()
            new_root.values.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
            node.values.insert(i + 1, value)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            child = node.values[i]
            if len(child.keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.values[i], key, value)

    def _split_child(self, parent, i):
        t = self.t
        node = parent.values[i]
        new_node = BPlusTreeNode(leaf=node.leaf)
        parent.keys.insert(i, node.keys[t - 1])
        parent.values.insert(i + 1, new_node)
        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]
        if node.leaf:
            new_node.values = node.values[t:]
            node.values = node.values[:t - 1]
            # 叶子节点链表
            new_node.next = getattr(node, 'next', None)
            node.next = new_node
        else:
            new_node.values = node.values[t:]
            node.values = node.values[:t]

    def range_query(self, low, high):
        result = []
        node = self.root
        # 找到最左的叶子节点
        while not node.leaf:
            node = node.values[0]
        while node:
            for k, v in zip(node.keys, node.values):
                if low <= k <= high:
                    result.append(v)
                elif k > high:
                    return result
            node = getattr(node, 'next', None)
        return result 

# ----------------- BTree 实现 -----------------
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.values = []  # 叶子节点存储值，内部节点存储子节点

class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(t, leaf=True)
        self.t = t

    def search(self, key, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            if node.leaf:
                return node.values[i]
            else:
                return self.search(key, node.values[i+1])
        if node.leaf:
            return None
        else:
            return self.search(key, node.values[i])

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t)
            new_root.values.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, key)
            node.values.insert(i + 1, value)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            child = node.values[i]
            if len(child.keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.values[i], key, value)

    def _split_child(self, parent, i):
        t = self.t
        node = parent.values[i]
        new_node = BTreeNode(t, leaf=node.leaf)
        parent.keys.insert(i, node.keys[t - 1])
        parent.values.insert(i + 1, new_node)
        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]
        if node.leaf:
            new_node.values = node.values[t:]
            node.values = node.values[:t - 1]
        else:
            new_node.values = node.values[t:]
            node.values = node.values[:t]

    def range_query(self, low, high):
        result = []
        self._range_query(self.root, low, high, result)
        return result

    def _range_query(self, node, low, high, result):
        i = 0
        while i < len(node.keys) and node.keys[i] < low:
            i += 1
        while i < len(node.keys) and node.keys[i] <= high:
            if node.leaf:
                result.append(node.values[i])
            else:
                self._range_query(node.values[i], low, high, result)
                # result.append(node.keys[i])  # 如果只存key可以加这行
            i += 1
        if not node.leaf and i < len(node.values):
            self._range_query(node.values[i], low, high, result) 
    
