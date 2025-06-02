from collections import defaultdict, deque
import numpy as np

class CustomerGraph:
    def __init__(self):
        self.graph = defaultdict(list)  # customer_name -> list of (neighbor, weight)
        self.reverse_graph = defaultdict(list)  # 反向邻接表（用于计算入度）
        self.customers = set()

    def add_customer(self, name):
        self.customers.add(name)

    def add_relation(self, from_name, to_name, weight):
        self.add_customer(from_name)
        self.add_customer(to_name)
        self.graph[from_name].append((to_name, weight))
        self.reverse_graph[to_name].append((from_name, weight))

    def remove_relation(self, from_name, to_name):
        self.graph[from_name] = [(n, w) for n, w in self.graph[from_name] if n != to_name]
        self.reverse_graph[to_name] = [(n, w) for n, w in self.reverse_graph[to_name] if n != from_name]

    def remove_customer(self, name):
        if name not in self.customers:
            raise ValueError("客户不存在")
        del self.graph[name]
        del self.reverse_graph[name]
        for n in self.customers:
            self.remove_relation(n, name)
        self.customers.remove(name)

    def update_relation(self, from_name, to_name, weight):
        self.remove_relation(from_name, to_name)
        self.add_relation(from_name, to_name, weight)

    def importance_scores(self, damping=0.85, max_iter=100, tol=1e-6):
        n = len(self.customers)
        if n == 0:
            return {}
        adj = defaultdict(dict)
        for c in self.customers:
            for neighbor, w in self.graph[c]:
                adj[c][neighbor] = w
        for c in self.customers:
            s = sum(w for w in adj[c].values())
            if s > 0:
                for neighbor in adj[c]:
                    adj[c][neighbor] /= s
        pr = {c: 1.0 / n for c in self.customers}
        for _ in range(max_iter):
            new_pr = {c: (1 - damping) / n for c in self.customers}
            for c in self.customers:
                for neighbor, w in adj[c].items():
                    new_pr[neighbor] += damping * pr[c] * w
            if sum(abs(new_pr[c] - pr[c]) for c in self.customers) < tol:
                break
            pr = new_pr
        return pr

    def influence_reach(self, name, min_weight=0, max_depth=None):
        if name not in self.customers:
            raise ValueError("客户不存在")
        reachable = set()
        q = deque([(name, 0)])
        while q:
            curr, depth = q.popleft()
            if max_depth is not None and depth > max_depth:
                continue
            for neighbor, w in self.graph[curr]:
                if w >= min_weight and neighbor not in reachable:
                    reachable.add(neighbor)
                    q.append((neighbor, depth + 1))
        return reachable

    def __repr__(self):
        return f"客户网络：{dict(self.graph)}"