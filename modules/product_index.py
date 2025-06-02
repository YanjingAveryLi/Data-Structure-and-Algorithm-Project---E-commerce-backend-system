from typing import List, Dict, Optional
from models import Product
import heapq
from collections import defaultdict

class ProductIndex:
    def __init__(self):
        self.products: Dict[str, Product] = {}  # id -> product
        self.name_index: Dict[str, str] = {}  # name -> id
        self.category_index: Dict[str, List[str]] = defaultdict(list)  # category -> [product_ids]
        self.price_index: List[tuple] = []  # (price, id) 用于价格区间查询
        self.popularity_index: List[tuple] = []  # (popularity, id) 用于热度排序
        self.trie = {}  # 前缀树，用于商品名称搜索

    def insert(self, product: Product):
        """插入商品"""
        if product.id in self.products:
            raise ValueError(f"商品ID {product.id} 已存在")
        self.products[product.id] = product
        self.name_index[product.name] = product.id
        self.category_index[product.category].append(product.id)
        heapq.heappush(self.price_index, (product.price, product.id))
        heapq.heappush(self.popularity_index, (-product.popularity, product.id))  # 大顶堆
        self._insert_to_trie(product.name, product)

    def delete(self, product_id: str):
        """删除商品"""
        if product_id not in self.products:
            raise ValueError("商品不存在")
        product = self.products[product_id]
        self.category_index[product.category].remove(product_id)
        self.name_index.pop(product.name, None)
        self.products.pop(product_id)
        # 重新构建索引（简单实现，数据量大时建议用更高效的方式）
        self.price_index = [(p, i) for (p, i) in self.price_index if i != product_id]
        heapq.heapify(self.price_index)
        self.popularity_index = [(-self.products[i].popularity, i) for i in self.products]
        heapq.heapify(self.popularity_index)
        

    def update(self, product_id: str, **kwargs):
        """修改商品信息"""
        if product_id not in self.products:
            raise ValueError("商品不存在")
        product = self.products[product_id]
        for k, v in kwargs.items():
            if hasattr(product, k):
                setattr(product, k, v)
        # 重新构建相关索引
        self.delete(product_id)
        self.insert(product)

    def _insert_to_trie(self, name: str, product: Product):
        """将商品名称插入前缀树"""
        node = self.trie
        for char in name.lower():
            if char not in node:
                node[char] = {"products": []}
            node = node[char]
            # 维护每个节点的热门商品列表（最多10个）
            products = node["products"]
            if len(products) < 10:
                heapq.heappush(products, (product.popularity, product.id))
            elif product.popularity > products[0][0]:
                heapq.heapreplace(products, (product.popularity, product.id))

    def search_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """按价格区间搜索商品"""
        result = []
        for price, pid in self.price_index:
            if min_price <= price <= max_price:
                result.append(self.products[pid])
        return sorted(result, key=lambda x: x.popularity, reverse=True)

    def search_by_category(self, category: str) -> List[Product]:
        """按类别搜索商品"""
        if category not in self.category_index:
            return []
        return [self.products[pid] for pid in self.category_index[category]]

    def search_by_prefix(self, prefix: str, limit: int = 10) -> List[Product]:
        """按前缀搜索商品（热度Top-K）"""
        node = self.trie
        for char in prefix.lower():
            if char not in node:
                return []
            node = node[char]
        # 获取该前缀下的热门商品
        products = []
        for popularity, pid in sorted(node["products"], reverse=True)[:limit]:
            products.append(self.products[pid])
        return products

    def search_by_id(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)

    def search_by_name(self, name: str) -> Optional[Product]:
        pid = self.name_index.get(name)
        return self.products.get(pid) if pid else None

    def update_stock(self, product_id: str, new_stock: int):
        if product_id not in self.products:
            raise ValueError("商品不存在")
        self.products[product_id].stock = new_stock

    def update_price(self, product_id: str, new_price: float):
        if product_id not in self.products:
            raise ValueError("商品不存在")
        self.products[product_id].price = new_price
        # 重新构建价格索引
        self.price_index = [(p, i) for (p, i) in self.price_index if i != product_id]
        heapq.heappush(self.price_index, (new_price, product_id))

    def get_product_statistics(self) -> Dict:
        return {
            "total_products": len(self.products),
            "categories": {cat: len(pids) for cat, pids in self.category_index.items()},
            "average_price": sum(p.price for p in self.products.values()) / len(self.products) if self.products else 0,
            "total_stock": sum(p.stock for p in self.products.values()),
            "top_categories": sorted(self.category_index.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        }
