from flask import Flask, render_template, request, jsonify
from data_generator import DataGenerator
from models import Product, Customer, CustomerRelation, MarketingTask, PagedProduct
from modules.task_scheduler import TaskScheduler
from modules.customer_network import CustomerNetwork
from modules.product_index import ProductIndex
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from db import Session
from Paged.paged_api import paged_api


app = Flask(__name__)

app.register_blueprint(paged_api)

generator = DataGenerator()
data = generator.generate_all_data()

task_scheduler = TaskScheduler()
customer_network = CustomerNetwork()
product_index = ProductIndex()

for product in data["products"]:
    product_index.insert(Product(**product))

for customer in data["customers"]:
    customer_network.add_customer(Customer(**customer))

for relation in data["relations"]:
    customer_network.add_relation(CustomerRelation(**relation))

for task in data["tasks"]:
    task_scheduler.insert(MarketingTask(**task))

for before_id, after_id in data["dependencies"]:
    task_scheduler.add_dependency(before_id, after_id)

@app.route("/")
def index():
    return render_template(
        "index.html",
        task_stats=task_scheduler.get_task_statistics(),
        network_stats=customer_network.get_network_statistics(),
        product_stats=product_index.get_product_statistics()

    )

@app.route("/products")
def products():
    """商品管理页面"""
    return render_template(
        "products.html",
        products=product_index.products.values(),
        categories=product_index.category_index.keys()
    )

@app.route("/products/search")
def search_products():
    """商品搜索接口"""
    query = request.args.get("q", "").strip()
    category = request.args.get("category")
    min_price_str = request.args.get("min_price", "")
    max_price_str = request.args.get("max_price", "")
    sort_by = request.args.get("sort_by", "popularity")  # 支持按热度、价格等排序

    min_price = float(min_price_str) if min_price_str else 0
    max_price = float(max_price_str) if max_price_str else float("inf")

    # 多条件组合查询
        # 初始结果用所有商品ID
    results = set(product_index.products.keys())

    if query:
        results &= set(p.id for p in product_index.search_by_prefix(query))
    if category:
        results &= set(p.id for p in product_index.search_by_category(category))
    if min_price > 0 or max_price < float("inf"):
        results &= set(p.id for p in product_index.search_by_price_range(min_price, max_price))

    # 排序
    products = [product_index.products[pid] for pid in results]
    if sort_by == "price":
        products.sort(key=lambda x: x.price)
    elif sort_by == "name":
        products.sort(key=lambda x: x.name)
    else:
        products.sort(key=lambda x: x.popularity, reverse=True)

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "brand": getattr(p, "brand", ""),
            "category": p.category,
            "price": p.price,
            "description": getattr(p, "description", ""),
            "image_url": getattr(p, "image_url", ""),
            "status": getattr(p, "status", ""),
            "sales": getattr(p, "sales", 0),
            "rating": getattr(p, "rating", 0),
            "popularity": p.popularity,
            "stock": p.stock
        }
        for p in products
    ])

@app.route("/products/<product_id>")
def product_detail(product_id):
    """商品详情页面"""
    product = product_index.search_by_id(product_id)
    if not product:
        return "商品不存在", 404
    return render_template("product_detail.html", product=product)

@app.route("/products/add", methods=["POST"])
def add_product():
    data = request.json
    try:
        product = Product(**data)
        product_index.insert(product)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/products/<product_id>/delete", methods=["POST"])
def delete_product(product_id):
    try:
        product_index.delete(product_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/products/<product_id>/update", methods=["POST"])
def update_product(product_id):
    data = request.json
    try:
        product_index.update(product_id, **data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/customers")
def customers():
    return render_template(
        "customers.html",
        customers=customer_network.customers.values(),
        importance=customer_network.calculate_customer_importance(),
        segments=customer_network.get_customer_segments()
    )

@app.route("/customers", methods=["GET"])
def get_customers():
    """获取所有客户信息"""
    return jsonify([c.__dict__ for c in customer_network.customers.values()])

@app.route("/customers", methods=["POST"])
def add_customer():
    """新增客户"""
    data = request.json
    customer = Customer(**data)
    customer_network.add_customer(customer)
    return jsonify({"status": "success"})

@app.route("/customers/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """修改客户信息"""
    data = request.json
    customer = customer_network.customers.get(customer_id)
    if not customer:
        return jsonify({"status": "error", "msg": "客户不存在"}), 404
    for k, v in data.items():
        if hasattr(customer, k):
            setattr(customer, k, v)
    return jsonify({"status": "success"})

@app.route("/customers/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """删除客户"""
    if customer_id not in customer_network.customers:
        return jsonify({"status": "error", "msg": "客户不存在"}), 404
    customer_network.customers.pop(customer_id)
    customer_network.adjacency_matrix.pop(customer_id, None)
    # 删除所有客户关系
    customer_network.relations = [rel for rel in customer_network.relations if rel.from_customer != customer_id and rel.to_customer != customer_id]
    for adj in customer_network.adjacency_matrix.values():
        adj.pop(customer_id, None)
    return jsonify({"status": "success"})

@app.route("/relations", methods=["POST"])
def add_relation():
    """新增客户关系"""
    data = request.json
    relation = CustomerRelation(**data)
    customer_network.add_relation(relation)
    return jsonify({"status": "success"})

@app.route("/relations", methods=["DELETE"])
def delete_relation():
    """删除客户关系"""
    data = request.json
    from_id = data["from_customer"]
    to_id = data["to_customer"]
    customer_network.relations = [rel for rel in customer_network.relations if not (rel.from_customer == from_id and rel.to_customer == to_id)]
    if from_id in customer_network.adjacency_matrix:
        customer_network.adjacency_matrix[from_id].pop(to_id, None)
    return jsonify({"status": "success"})

@app.route("/customers/graph")
def get_customer_graph():
    """获取客户网络图数据（节点+边）"""
    return jsonify(customer_network.get_graph_data())

@app.route("/customers/pagerank")
def get_customer_pagerank():
    """获取客户PageRank影响力评分"""
    pr = customer_network.calculate_customer_importance(method="pagerank")
    return jsonify(pr)

@app.route("/customers/centrality")
def get_customer_centrality():
    """获取客户度中心性评分"""
    centrality = customer_network.calculate_customer_importance(method="degree")
    return jsonify(centrality)

@app.route("/customers/propagation")
def get_customer_propagation():
    """影响力传播模拟"""
    source_id = request.args.get("source_id")
    max_depth = int(request.args.get("max_depth", 3))
    min_weight = float(request.args.get("min_weight", 0.1))
    result = customer_network.get_customer_influence(source_id, min_weight, max_depth)
    return jsonify(list(result))

@app.route("/customers/statistics")
def get_customer_statistics():
    """获取客户网络统计信息"""
    return jsonify(customer_network.get_network_statistics())

# ------------------ 客户网络管理页面 ------------------

@app.route("/customer_network")
def customer_network_page():
    return render_template("customer_network.html")

@app.route("/tasks", methods=["POST"])
def add_task():
    """插入任务"""
    data = request.json
    task = MarketingTask(
        id=data["id"],
        name=data["name"],
        urgency=float(data["urgency"]),
        influence=float(data["influence"]),
        priority=float(data["urgency"]) * float(data["influence"]),
        created_date=data.get("created_date", datetime.now().strftime("%Y-%m-%d"))
    )
    task_scheduler.insert(task)
    return jsonify({"status": "success"})

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """删除任务"""
    try:
        task_scheduler.delete(task_id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 400

@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    """修改任务"""
    data = request.json
    try:
        task_scheduler.update(task_id, **data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 400

@app.route("/tasks/<task_id>/dependencies", methods=["POST"])
def set_dependency(task_id):
    """设置依赖"""
    data = request.json
    before_id = data["before_id"]
    try:
        task_scheduler.add_dependency(before_id, task_id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 400

@app.route("/tasks/<task_id>/dependencies", methods=["DELETE"])
def remove_dependency(task_id):
    """移除依赖"""
    data = request.json
    before_id = data["before_id"]
    try:
        task_scheduler.remove_dependency(before_id, task_id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 400

@app.route("/tasks/topk")
def topk_tasks():
    """查看前k个任务"""
    k = int(request.args.get("k", 5))
    tasks = task_scheduler.top_k_tasks(k)
    return jsonify([task.__dict__ for task in tasks])

@app.route("/tasks/execute", methods=["POST"])
def execute_task():
    """执行优先级最高的可执行任务"""
    task = task_scheduler.execute_highest_priority()
    if task:
        # 返回最新的可执行任务列表
        tasks = [t.__dict__ for t in task_scheduler.top_k_tasks(10)]
        return jsonify({"status": "success", "executed_task": task.__dict__, "tasks": tasks})
    else:
        return jsonify({"status": "no_task"})

@app.route("/tasks/dag")
def get_dag():
    """获取DAG数据用于前端可视化"""
    return jsonify(task_scheduler.get_dependencies_graph())

# ------------------ 任务管理页面渲染 ------------------

@app.route("/tasks")
def tasks():
    """任务管理页面"""
    k = int(request.args.get("k", 10))
    return render_template(
        "tasks.html",
        tasks=task_scheduler.top_k_tasks(k),
        task_stats=task_scheduler.get_task_statistics()
    )
# 批量插入商品
@app.route('/paged_products/batch_add', methods=['POST'])
def paged_batch_add_products():
    session = Session()
    products = request.json['products']
    objs = [PagedProduct(**p) for p in products]
    session.bulk_save_objects(objs)
    session.commit()
    return jsonify({'status': 'success', 'count': len(objs)})

# 分页查询商品
@app.route('/paged_products')
def paged_products():
    return render_template('paged_products.html')

# 批量删除商品
@app.route('/paged_products/batch_delete', methods=['POST'])
def paged_batch_delete_products():
    session = Session()
    ids = request.json['ids']
    session.query(PagedProduct).filter(PagedProduct.paged_id.in_(ids)).delete(synchronize_session=False)
    session.commit()
    return jsonify({'status': 'success', 'count': len(ids)})

# 批量更新商品
@app.route('/paged_products/batch_update', methods=['POST'])
def paged_batch_update_products():
    session = Session()
    updates = request.json['updates']  # [{'paged_id':..., 'paged_price':..., ...}, ...]
    for upd in updates:
        session.query(PagedProduct).filter(PagedProduct.paged_id == upd['paged_id']).update(upd)
    session.commit()
    return jsonify({'status': 'success', 'count': len(updates)})

@app.route('/api/paged_products')
def api_paged_products():
    # 这里写分页查询逻辑，返回 JSON
    # 例如：
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    sort_by = request.args.get('sort_by', 'paged_popularity')
    # 其他筛选条件...
    session = Session()
    query = session.query(PagedProduct)
    total = query.count()
    products = query.order_by(getattr(PagedProduct, sort_by).desc()) \
                    .offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'products': [p.to_dict() for p in products],
        'total': total
    })

@app.route('/api/recommend_tree', methods=['POST'])
def recommend_tree():
    data = request.json
    n = data.get('n', 20)
    mode = data.get('mode', 'min')
    k = data.get('k', None)
    generator = DataGenerator()
    result = generator.generate_product_edges_and_mst(n=n, mode=mode, k=k)
    return jsonify(result)

@app.route('/recommand')
def recommand():
    return render_template('recommand.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
