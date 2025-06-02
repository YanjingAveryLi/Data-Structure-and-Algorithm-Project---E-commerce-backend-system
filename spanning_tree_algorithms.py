# UnionFind class 不相交集
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # 每个节点的父节点
        self.rank = [0] * n  # 用来优化合并的秩
    
    def find(self, x):  # 查找操作，获得根节点
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]
    
    def union(self, x, y):  # 合并操作
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            # 合并时使用秩优化
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1


def merge_sort(arr):  
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort(left)
        merge_sort(right)
        
        i = j = k = 0
        while i < len(left) and j < len(right):
            # 按照权重排序
            # 比如a问红色边权重为0，蓝色边权重为1
            # 比如b问红色边权重为1，蓝色边权重为0
            if left[i][3] < right[j][3]:  
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr



def kruskal_min_blue_edges(n, edges):  # 未改进的算法
    # 在每条边中加入权重信息，红色边权重为0，蓝色边权重为1
    # 此时的kruskal算法即优先选择红色边（权重为0，更小）
    weighted_edges = []
    for u, v, color in edges:
        weight = 0 if color == 'red' else 1  # 红色边权重为0，蓝色边权重为1
        weighted_edges.append((u, v, color, weight))

    # 使用Merge Sort对边进行排序
    sorted_edges = merge_sort(weighted_edges)

    uf = UnionFind(n)  # 初始化并查集
    mst = []  # 最小生成树
    blue_count = 0  # 蓝色边数量
    
    for u, v, color, weight in sorted_edges:
        if uf.find(u) != uf.find(v):  # 如果不形成环
            uf.union(u, v)  # 合并两个集合
            mst.append((u, v, color))  # 将该边加入生成树
            if color == 'blue':  # 如果是蓝色边
                blue_count += 1
    
    return mst, blue_count


def kruskal_min_blue_edges_improve(n, edges):  # 改进后的算法
    # 改进后不使用merge排序，而是直接检测是否是蓝色边/红色边
    red_edges = [e for e in edges if e[2] == 'red']
    blue_edges = [e for e in edges if e[2] == 'blue']

    uf = UnionFind(n)  # 初始化并查集
    mst = []  # 最小生成树
    blue_count = 0  # 蓝色边数量
    
    # 先处理所有红色边
    for u, v, color in red_edges:
        if uf.find(u) != uf.find(v):  # 如果不形成环
            uf.union(u, v)  # 合并两个集合
            mst.append((u, v, color))  # 将该边加入生成树
    
    # 之后处理蓝色边
    for u, v, color in blue_edges:
        if uf.find(u) != uf.find(v):  # 如果不形成环
            uf.union(u, v)  # 合并两个集合
            mst.append((u, v, color))  # 将该边加入生成树
            blue_count +=1

    return mst, blue_count


def kruskal_max_blue_edges(n, edges):
    # 在每条边中加入权重信息，红色边权重为1，蓝色边权重为0
    # 此时的kruskal算法即优先选择蓝色边（权重为0，更小）
    weighted_edges = []
    for u, v, color in edges:
        weight = 0 if color == 'blue' else 1  # 蓝色边权重为0，红色边权重为1
        weighted_edges.append((u, v, color, weight))

    # 使用Merge Sort对边进行排序
    sorted_edges = merge_sort(weighted_edges)

    uf = UnionFind(n)  # 初始化并查集
    mst = []  # 最小生成树
    blue_count = 0  # 蓝色边数量
    
    for u, v, color, weight in sorted_edges:
        if uf.find(u) != uf.find(v):  # 如果不形成环
            uf.union(u, v)  # 合并两个集合
            mst.append((u, v, color))  # 将该边加入生成树
            if color == 'blue':  # 如果是蓝色边
                blue_count += 1
    
    return mst, blue_count


def first_kruskal(n, edges):
    # 第1次Kruskal：优先使用红色边，然后使用蓝色边，找到所必须的蓝色边
    red_edges = [e for e in edges if e[2] == 'red']
    blue_edges = [e for e in edges if e[2] == 'blue']
    
    uf = UnionFind(n)
    required_blue = set()
    total_edges = 0
    
    # 先处理所有红色边
    for u, v, _ in red_edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            total_edges += 1
    
    # 处理蓝色边
    for u, v, _ in blue_edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            required_blue.add((u, v))
            total_edges += 1
    
    # 检查是否形成了生成树
    if total_edges != n - 1:
        return None, None  # 无法形成生成树
    
    return required_blue


def second_kruskal(n, edges, required_blue, k):
    # 第2次Kruskal：使用必需的蓝色边，然后优先选择剩余的蓝色边，最后用红色边补足
    b1 = len(required_blue) # 必须至少有b1个蓝边，才可以形成连通图
    all_edges = [] # 用来储存最后恰好有k个蓝边的树的节点，为了之后作图用；若仅判断能否生成则无需储存该变量
    
    if b1 > k:
        return False  # 必需的蓝色边数量已经超过k
    
    # 初始化并查集
    uf = UnionFind(n)
    
    # 添加必需的蓝色边
    blue_count = 0
    for u, v in required_blue:
        uf.union(u, v)
        all_edges.append((u, v, 'blue'))  # 做图用，因此储存
        blue_count += 1
    
    # 收集剩余的蓝色边和红色边，将其分别放在不同的数组中
    remaining_blue = []
    red_edges = []
    for u, v, color in edges:
        if color == 'blue':
            if (u, v) not in required_blue and (v, u) not in required_blue:
                remaining_blue.append((u, v))
        else:
            red_edges.append((u, v))
    
    # 优先选择蓝色变，尝试添加剩余的蓝色边，直到达到k-b1条
    for u, v in remaining_blue:
        if blue_count >= k:
            break
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            all_edges.append((u, v, 'blue'))  # 做图用，因此储存
            blue_count += 1
    
    # 如果蓝色边数量不足k，返回False，说明不可以生成恰好k条蓝边的树
    if blue_count < k:
        return False
    
    # 最后添加红色边，直到形成生成树
    for u, v in red_edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            all_edges.append((u, v, 'red'))  # 做图用，因此储存
    
    # 检查是否所有节点都连通
    root = uf.find(0)
    for i in range(1, n):
        if uf.find(i) != root:
            return False  # 图不连通
    
    return all_edges  # 存在符合条件的生成树；若无需做图，则return True即可



def kruskal_two_stage(n, edges, k):
    required_blue = first_kruskal(n, edges)
    if required_blue is None:
        print(f"无法形成生成树")
        return False
    
    all_edges = second_kruskal(n, edges, required_blue, k)

    if second_kruskal(n, edges, required_blue, k):
        print(f"存在符合条件的生成树，包含{k}条蓝色边")
        return(all_edges)
    
    else:
        print(f"不存在符合条件的生成树")
        return False
