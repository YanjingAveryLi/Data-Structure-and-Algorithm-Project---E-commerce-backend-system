from flask import Blueprint, request, jsonify
from .paged_utils import get_paged_products, batch_add_paged_products, batch_delete_paged_products, batch_update_paged_products

paged_api = Blueprint('paged_api', __name__, url_prefix='/api')

@paged_api.route('/paged_products', methods=['GET'])
def api_get_paged_products():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    sort_by = request.args.get('sort_by', 'paged_popularity')
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    total, products = get_paged_products(page, page_size, sort_by, category, min_price, max_price)
    return jsonify({
        'total': total,
        'products': [
            {
                'paged_id': p.paged_id,
                'paged_name': p.paged_name,
                'paged_category': p.paged_category,
                'paged_price': p.paged_price,
                'paged_popularity': p.paged_popularity,
                'paged_stock': p.paged_stock,
                'paged_status': p.paged_status,
                'paged_sales': p.paged_sales,
                'paged_rating': p.paged_rating,
                'paged_description': p.paged_description,
                'paged_image_url': p.paged_image_url
            } for p in products
        ]
    })

@paged_api.route('/paged_products/batch_add', methods=['POST'])
def api_batch_add_paged_products():
    products = request.json['products']
    count = batch_add_paged_products(products)
    return jsonify({'status': 'success', 'count': count})

@paged_api.route('/paged_products/batch_delete', methods=['POST'])
def api_batch_delete_paged_products():
    ids = request.json['ids']
    count = batch_delete_paged_products(ids)
    return jsonify({'status': 'success', 'count': count})

@paged_api.route('/paged_products/batch_update', methods=['POST'])
def api_batch_update_paged_products():
    updates = request.json['updates']
    count = batch_update_paged_products(updates)
    return jsonify({'status': 'success', 'count': count})
