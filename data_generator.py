import random
from datetime import datetime, timedelta
import string


class DataGenerator:
    def __init__(self):
        # 预定义一些电商相关的数据
        self.product_categories = [
            "Electronics", "Clothing", "Home & Garden", "Sports", "Books",
            "Toys", "Beauty", "Automotive", "Jewelry", "Health"
        ]
        
        self.product_brands = {
            "Electronics": ["Apple", "Samsung", "Sony", "LG", "Dell"],
            "Clothing": ["Nike", "Adidas", "Zara", "H&M", "Uniqlo"],
            "Home & Garden": ["IKEA", "Home Depot", "Wayfair", "Target", "Walmart"],
            "Sports": ["Nike", "Adidas", "Under Armour", "Puma", "New Balance"],
            "Books": ["Penguin", "HarperCollins", "Random House", "Scholastic", "Simon & Schuster"],
            "Toys": ["LEGO", "Hasbro", "Mattel", "Fisher-Price", "Disney"],
            "Beauty": ["L'Oreal", "MAC", "Estee Lauder", "Clinique", "Maybelline"],
            "Automotive": ["Toyota", "Honda", "Ford", "BMW", "Mercedes"],
            "Jewelry": ["Tiffany", "Cartier", "Pandora", "Swarovski", "Bvlgari"],
            "Health": ["Johnson & Johnson", "Pfizer", "Bayer", "GSK", "Merck"]
        }
        
        self.customer_types = ["Regular", "Premium", "VIP", "Wholesale"]
        self.payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Alipay", "WeChat Pay"]
        self.shipping_methods = ["Standard", "Express", "Next Day", "International"]

    def generate_product_name(self, category):
        """生成真实的商品名称"""
        brand = random.choice(self.product_brands[category])
        if category == "Electronics":
            models = ["Pro", "Max", "Lite", "Plus", "Elite"]
            return f"{brand} {random.choice(models)} {random.randint(1000, 9999)}"
        elif category == "Clothing":
            styles = ["Classic", "Modern", "Vintage", "Casual", "Formal"]
            return f"{brand} {random.choice(styles)} {random.choice(['Shirt', 'Dress', 'Jacket', 'Pants'])}"
        else:
            return f"{brand} {category} Item {random.randint(1, 1000)}"

    def generate_products(self, n=50):
        """生成丰富的商品数据"""
        products = []
        for i in range(n):
            category = random.choice(self.product_categories)
            brand = random.choice(self.product_brands[category])
            name = self.generate_product_name(category)
            base_price = random.uniform(10.0, 1000.0)
            if "Apple" in name or "Tiffany" in name:
                base_price *= 2
            price = round(base_price, 2)
            popularity = int(1000 / (price + 1) * random.uniform(0.5, 2.0))
            stock = random.randint(0, 1000)
            status = random.choice(["在售", "下架", "预售"])
            sales = random.randint(0, 5000)
            rating = round(random.uniform(3.0, 5.0), 2)
            description = f"{brand} {category}，高品质，热销推荐，{random.choice(['限时特价', '新品上市', '爆款热卖'])}。"
            image_url = f"https://dummyimage.com/200x200/cccccc/000000&text={brand}"
            products.append({
                "id": f"PROD{i:05d}",
                "name": name,
                "brand": brand,
                "category": category,
                "price": price,
                "popularity": popularity,
                "stock": stock,
                "status": status,
                "sales": sales,
                "rating": rating,
                "description": description,
                "image_url": image_url,
                "created_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
            })
        return products
    
    def generate_paged_products(self,n=1000):
        """生成分页商品数据（适配PagedProduct ORM）"""
        products = []
        for i in range(n):
            products.append({
                "paged_id": f"PROD{i:05d}",
                "paged_name": f"Product {i}",
                "paged_category": random.choice(["Electronics", "Clothing", "Books", "Toys"]),
                "paged_price": round(random.uniform(10, 1000), 2),
                "paged_popularity": random.randint(1, 1000),
                "paged_stock": random.randint(0, 1000),
                "paged_status": random.choice(["在售", "下架"]),
                "paged_sales": random.randint(0, 5000),
                "paged_rating": round(random.uniform(3.0, 5.0), 2),
                "paged_description": f"Description for product {i}",
                "paged_image_url": ""
            })
        return products
        
    def random_name(self):
        first_names = ['张', '李', '王', '赵', '刘', '陈', '杨', '黄', '周', '吴']
        last_names = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋']
        return random.choice(first_names) + random.choice(last_names)

    def random_phone(self):
        return "1" + "".join([str(random.randint(0, 9)) for _ in range(10)])

    def random_email(self,name):
        domains = ['@qq.com', '@163.com', '@gmail.com', '@outlook.com']
        return f"{name.lower()}{random.randint(100,999)}{random.choice(domains)}"

    def random_region(self):
        regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '重庆', '南京', '苏州', '武汉']
        return random.choice(regions)

    def generate_customers(self, n=30):
        """生成更真实的客户数据"""
        customers = []
        for i in range(n):
            customer_type = random.choice(self.customer_types)
            gender = random.choice(['男', '女'])
            age = random.randint(18, 60)
            name = self.random_name()
            phone = self.random_phone()
            email = self.random_email(name)
            region = self.random_region()
            # 影响力相关属性
            if customer_type == "VIP":
                purchase_power = random.uniform(0.8, 1.0)
                activity_level = random.uniform(0.7, 1.0)
            elif customer_type == "Premium":
                purchase_power = random.uniform(0.6, 0.9)
                activity_level = random.uniform(0.5, 0.8)
            else:
                purchase_power = random.uniform(0.3, 0.7)
                activity_level = random.uniform(0.2, 0.6)
            customers.append({
                "id": f"CUST{i:04d}",
                "name": name,
                "gender": gender,
                "age": age,
                "phone": phone,
                "email": email,
                "region": region,
                "type": customer_type,
                "purchase_power": round(purchase_power, 2),
                "activity_level": round(activity_level, 2),
                "join_date": (datetime.now() - timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d")
            })
        return customers

    def generate_relations(self, customers, n_relations=50):
        """生成丰富的客户关系数据"""
        relations = []
        relation_types = ["推荐", "合作", "共同购买", "评价互动", "好友", "同地区"]
        for _ in range(n_relations):
            from_cust = random.choice(customers)
            to_cust = random.choice(customers)
            if from_cust != to_cust:
                # 影响力权重可结合购买力、活跃度、客户类型等
                base_weight = (from_cust["activity_level"] + to_cust["activity_level"]) / 2
                if from_cust["region"] == to_cust["region"]:
                    base_weight += 0.1  # 同地区关系更强
                if from_cust["type"] == "VIP" or to_cust["type"] == "VIP":
                    base_weight += 0.1
                weight = min(round(base_weight * random.uniform(0.8, 1.2), 2), 1.0)
                relations.append({
                    "from_customer": from_cust["id"],
                    "to_customer": to_cust["id"],
                    "weight": weight,
                    "relation_type": random.choice(relation_types)
                })
        return relations

    def generate_tasks_with_dependencies(self,n=20):
        """生成带有依赖关系的电商营销任务数据"""
        task_templates = [
            ("大促活动", [
                "618大促首页Banner投放",
                "双11预热邮件营销",
                "年终大促专题页设计",
                "黑五限时折扣活动"
            ]),
            ("库存补货", [
                "爆款商品库存补货",
                "滞销品清仓活动",
                "热销品紧急补货",
                "仓库盘点与补货"
            ]),
            ("新用户拉新", [
                "新用户拉新短信推送",
                "新用户专属优惠券发放",
                "新用户注册奖励活动",
                "新用户首单引导"
            ]),
            ("客户关怀", [
                "高价值客户专属优惠券发放",
                "老客户回访关怀",
                "客户节日祝福推送",
                "售后服务满意度回访"
            ]),
            ("商品上新", [
                "新品发布推送",
                "新品上架Banner设计",
                "新品试用活动",
                "新品直播带货"
            ]),
            ("价格调整", [
                "爆款商品限时降价",
                "滞销品价格调整",
                "全场满减活动",
                "会员专属折扣调整"
            ]),
            ("售后服务", [
                "退货退款处理",
                "售后服务满意度回访",
                "投诉处理专员分配",
                "售后问题自动分派"
            ])
        ]

        tasks = []
        dependencies = []  # (before_id, after_id) 依赖对

        for i in range(n):
            task_type, name_list = random.choice(task_templates)
            name = random.choice(name_list)
            if task_type in ["大促活动", "新用户拉新"]:
                base_urgency = random.uniform(0.8, 1.0)
                base_influence = random.uniform(0.7, 1.0)
            elif task_type in ["库存补货", "价格调整"]:
                base_urgency = random.uniform(0.6, 0.9)
                base_influence = random.uniform(0.5, 0.8)
            elif task_type == "客户关怀":
                base_urgency = random.uniform(0.5, 0.8)
                base_influence = random.uniform(0.4, 0.7)
            elif task_type == "商品上新":
                base_urgency = random.uniform(0.5, 0.8)
                base_influence = random.uniform(0.5, 0.8)
            else:  # 售后服务
                base_urgency = random.uniform(0.6, 0.9)
                base_influence = random.uniform(0.4, 0.7)

            task_id = f"TASK{i:04d}"
            tasks.append({
                "id": task_id,
                "name": name,
                "type": task_type,
                "urgency": round(base_urgency, 2),
                "influence": round(base_influence, 2),
                "priority": round(base_urgency * base_influence, 2),
                "created_date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            })

            # 依赖生成逻辑：每个任务有80%概率依赖2~4个前面的任务
            if i > 0 and random.random() < 0.8:
                max_deps = min(4, i)
                if max_deps >= 2:
                    num_deps = random.randint(2, max_deps)
                    dep_indices = random.sample(range(i), num_deps)
                    for dep_idx in dep_indices:
                        before_id = f"TASK{dep_idx:04d}"
                        dependencies.append((before_id, task_id))
                else:
                    # 只有1个可选前置任务时，最多依赖1个
                    dep_indices = random.sample(range(i), 1)
                    for dep_idx in dep_indices:
                        before_id = f"TASK{dep_idx:04d}"
                        dependencies.append((before_id, task_id))

        return tasks, dependencies

    def generate_all_data(self):
        """生成所有数据"""
        products = self.generate_products(50)
        customers = self.generate_customers(30)
        relations = self.generate_relations(customers, 50)
        tasks, dependencies = self.generate_tasks_with_dependencies(20)
        
        return {
            "products": products,
            "customers": customers,
            "relations": relations,
            "tasks": tasks,
            "dependencies": dependencies
        }

    def generate_product_edges_and_mst(self, n=20, mode='min', k=None, max_edges_per_node=3):
        """
        生成商品数据、商品关系边，并融合生成树算法，返回前端可用的节点和边
        mode: 'min'（相关性优先）、'max'（多样性优先）、'exact'（恰好k条蓝色边）
        """
        products = self.generate_products(n)
        edges = []
        for i in range(n):
            count = 0
            for j in range(n):
                if i == j:
                    continue
                p1, p2 = products[i], products[j]
                # 强相关：同类别
                if p1['category'] == p2['category']:
                    color = 'red'
                else:
                    color = 'blue'
                # 控制每个商品的边数，避免全连接
                if color == 'red' and random.random() < 0.5:
                    edges.append((i, j, color))
                    count += 1
                elif color == 'blue' and random.random() < 0.1:
                    edges.append((i, j, color))
                    count += 1
                if count >= max_edges_per_node:
                    break
        # 选择生成树算法
        if mode == 'min':
            from spanning_tree_algorithms import kruskal_min_blue_edges
            mst, blue_count = kruskal_min_blue_edges(n, edges)
        elif mode == 'max':
            from spanning_tree_algorithms import kruskal_max_blue_edges
            mst, blue_count = kruskal_max_blue_edges(n, edges)
        elif mode == 'exact':
            from spanning_tree_algorithms import kruskal_two_stage
            mst = kruskal_two_stage(n, edges, k)
            blue_count = k if mst else 0
        else:
            raise ValueError('Invalid mode')
        # 节点
        nodes = [
            {
                "id": i,
                "label": products[i]['name'],
                "category": products[i]['category'],
                "image": products[i]['image_url'],
                "title": f"{products[i]['name']}<br>价格: {products[i]['price']}<br>品牌: {products[i]['brand']}"
            }
            for i in range(n)
        ]
        # 边（只用生成树中的边）
        edges_for_frontend = [
            {
                "from": u,
                "to": v,
                "color": "red" if color == "red" else "blue",
                "width": 2 if color == "red" else 1
            }
            for (u, v, color) in mst
        ]
        return {
            "nodes": nodes,
            "edges": edges_for_frontend,
            "blue_count": blue_count
        }

# 测试代码
if __name__ == "__main__":
    generator = DataGenerator()
    data = generator.generate_all_data()
    paged_products = generator.generate_paged_products(1000)
    import json
    with open("paged_products.json", "w", encoding="utf-8") as f:
        json.dump(paged_products, f, ensure_ascii=False, indent=2)
    print("已生成分页商品数据！")
    
    result = generator.generate_product_edges_and_mst(n=10, mode='min')
    with open("product_network.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("已生成商品网络生成树数据！")
    print("节点示例：", result["nodes"][:2])
    print("边示例：", result["edges"][:2])

    print("\n=== 商品数据示例 ===")
    for product in data["products"][:3]:
        print(f"商品: {product['name']}")
        print(f"类别: {product['category']}")
        print(f"价格: ${product['price']}")
        print(f"热度: {product['popularity']}")
        print(f"库存: {product['stock']}")
        print(f"创建日期: {product['created_date']}")
        print()
    
    print("\n=== 客户数据示例 ===")
    for customer in data["customers"][:3]:
        print(f"客户ID: {customer['id']}")
        print(f"类型: {customer['type']}")
        print(f"购买力: {customer['purchase_power']}")
        print(f"活跃度: {customer['activity_level']}")
        print(f"加入日期: {customer['join_date']}")
        print()
    
    print("\n=== 客户关系示例 ===")
    for relation in data["relations"][:3]:
        print(f"从: {relation['from_customer']}")
        print(f"到: {relation['to_customer']}")
        print(f"权重: {relation['weight']}")
        print(f"关系类型: {relation['relation_type']}")
        print()
    
    print("\n=== 营销任务示例 ===")
    for task in data["tasks"][:3]:
        print(f"任务ID: {task['id']}")
        print(f"名称: {task['name']}")
        print(f"类型: {task['type']}")
        print(f"紧急度: {task['urgency']}")
        print(f"影响力: {task['influence']}")
        print(f"优先级: {task['priority']}")
        print(f"创建日期: {task['created_date']}")
        print()