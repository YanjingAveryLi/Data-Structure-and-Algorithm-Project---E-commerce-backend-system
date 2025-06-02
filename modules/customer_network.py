from typing import Dict, List, Set, Any
from models import Customer, CustomerRelation

class CustomerNetwork:
    def __init__(self):
        self.customers: Dict[str, Customer] = {}  # 客户ID -> Customer对象
        self.relations: List[CustomerRelation] = []  # 所有关系
        self.adjacency_matrix: Dict[str, Dict[str, float]] = {}  # from_id -> {to_id: weight}

    # 客户管理
    def add_customer(self, customer: Customer):
        self.customers[customer.id] = customer
        if customer.id not in self.adjacency_matrix:
            self.adjacency_matrix[customer.id] = {}

    def update_customer(self, customer_id: str, **kwargs):
        customer = self.customers.get(customer_id)
        if not customer:
            raise ValueError("客户不存在")
        for k, v in kwargs.items():
            if hasattr(customer, k):
                setattr(customer, k, v)

    def delete_customer(self, customer_id: str):
        if customer_id not in self.customers:
            raise ValueError("客户不存在")
        self.customers.pop(customer_id)
        self.adjacency_matrix.pop(customer_id, None)
        # 删除所有与该客户相关的关系
        self.relations = [rel for rel in self.relations if rel.from_customer != customer_id and rel.to_customer != customer_id]
        for adj in self.adjacency_matrix.values():
            adj.pop(customer_id, None)

    # 关系管理
    def add_relation(self, relation: CustomerRelation):
        if relation.from_customer not in self.customers or relation.to_customer not in self.customers:
            raise ValueError("客户不存在")
        self.relations.append(relation)
        self.adjacency_matrix[relation.from_customer][relation.to_customer] = relation.weight

    def delete_relation(self, from_id: str, to_id: str):
        self.relations = [rel for rel in self.relations if not (rel.from_customer == from_id and rel.to_customer == to_id)]
        if from_id in self.adjacency_matrix:
            self.adjacency_matrix[from_id].pop(to_id, None)

    # 影响力分析
    def calculate_customer_importance(self, method: str = "pagerank") -> Dict[str, float]:
        if method == "pagerank":
            return self._calculate_pagerank()
        elif method == "degree":
            return self._calculate_degree_centrality()
        else:
            raise ValueError("不支持的重要性计算方法")

    def _calculate_pagerank(self, damping: float = 0.85, max_iter: int = 100) -> Dict[str, float]:
        n = len(self.customers)
        if n == 0:
            return {}
        # 构建转移矩阵
        transition_matrix = {}
        for from_cust in self.customers:
            transition_matrix[from_cust] = {}
            total_weight = sum(self.adjacency_matrix[from_cust].values())
            if total_weight > 0:
                for to_cust, weight in self.adjacency_matrix[from_cust].items():
                    transition_matrix[from_cust][to_cust] = weight / total_weight
        # 初始化PageRank值
        pr = {cust_id: 1.0 / n for cust_id in self.customers}
        for _ in range(max_iter):
            new_pr = {cust_id: (1 - damping) / n for cust_id in self.customers}
            for from_cust in self.customers:
                for to_cust, weight in transition_matrix.get(from_cust, {}).items():
                    new_pr[to_cust] += damping * pr[from_cust] * weight
            pr = new_pr
        # 可选：将分数写回Customer对象
        for cust_id, score in pr.items():
            setattr(self.customers[cust_id], "score", round(score, 4))
        return pr

    def _calculate_degree_centrality(self) -> Dict[str, float]:
        centrality = {}
        for cust_id in self.customers:
            in_degree = sum(1 for rel in self.relations if rel.to_customer == cust_id)
            out_degree = sum(1 for rel in self.relations if rel.from_customer == cust_id)
            centrality[cust_id] = (in_degree + out_degree) / (2 * (len(self.customers) - 1)) if len(self.customers) > 1 else 0
        return centrality

    # 影响力传播模拟
    def get_customer_influence(self, customer_id: str, min_weight: float = 0.1, max_depth: int = 3) -> Set[str]:
        if customer_id not in self.customers:
            raise ValueError("客户不存在")
        influenced = set()
        to_visit = [(customer_id, 0, 1.0)]  # (customer_id, depth, path_weight)
        while to_visit:
            current, depth, path_weight = to_visit.pop(0)
            if depth > max_depth or path_weight < min_weight:
                continue
            for neighbor, weight in self.adjacency_matrix.get(current, {}).items():
                new_weight = path_weight * weight
                if new_weight >= min_weight and neighbor not in influenced:
                    influenced.add(neighbor)
                    to_visit.append((neighbor, depth + 1, new_weight))
        return influenced

    # 分群
    def get_customer_segments(self) -> Dict[str, List[str]]:
        segments = {}
        for cust_id, customer in self.customers.items():
            if customer.type not in segments:
                segments[customer.type] = []
            segments[customer.type].append(cust_id)
        return segments

    # 网络统计
    def get_network_statistics(self) -> Dict[str, Any]:
        return {
            "total_customers": len(self.customers),
            "total_relations": len(self.relations),
            "average_relations": len(self.relations) / len(self.customers) if self.customers else 0,
            "customer_types": {t: len([c for c in self.customers.values() if c.type == t])
                               for t in set(c.type for c in self.customers.values())}
        }

    # 前端可视化友好
    def get_graph_data(self):
        nodes = []
        for cust_id, customer in self.customers.items():
            nodes.append({
                "id": cust_id,
                "label": customer.name,
                "type": customer.type,
                "purchase_power": getattr(customer, "purchase_power", None),
                "activity_level": getattr(customer, "activity_level", None),
                "gender": getattr(customer, "gender", None),
                "age": getattr(customer, "age", None),
                "region": getattr(customer, "region", None),
                "score": getattr(customer, "score", 0)
            })
        edges = []
        for rel in self.relations:
            edges.append({
                "from": rel.from_customer,
                "to": rel.to_customer,
                "weight": rel.weight,
                "relation_type": getattr(rel, "relation_type", "关系")
            })
        return {"nodes": nodes, "edges": edges}