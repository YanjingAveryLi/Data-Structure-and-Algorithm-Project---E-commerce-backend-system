from modules.bplustree import BPlusTree
from modules.avl_tree import AVLTree
from modules.bplustree import BTree
from modules.lsmtree import LSMTree

tree = BPlusTree(t=3)  # t为阶数，3为最小可用
tree.insert(1001, "商品A")
tree.insert(1002, "商品B")
print(tree.search(1001))  # 输出: 商品A
print(tree.range_query(1000, 2000))  # 输出区间内所有商品

tree = AVLTree()
tree.insert(1001, "商品A")
tree.insert(1002, "商品B")
print(tree.search(1001))  # 输出: 商品A
print(tree.range_query(1000, 2000))  # 输出区间内所有商品

tree = LSMTree(memtable_limit=3)
tree.insert(1001, "商品A")
tree.insert(1002, "商品B")
tree.insert(1003, "商品C")  # 触发flush
tree.insert(1004, "商品D")
print(tree.search(1002))  # 输出: 商品B
print(tree.range_query(1000, 2004))  # 输出区间内所有商品

tree = BTree(t=3)
tree.insert(1001, "商品A")
tree.insert(1002, "商品B")
print(tree.search(1001))  # 输出: 商品A
print(tree.range_query(1000, 2000))  # 输出区间内所有商品



