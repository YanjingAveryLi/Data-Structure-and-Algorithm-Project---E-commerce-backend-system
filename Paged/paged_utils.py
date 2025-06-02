from db import Session
from models import PagedProduct

def get_paged_products(page=1, page_size=20, sort_by='paged_popularity', category=None, min_price=None, max_price=None):
    session = Session()
    query = session.query(PagedProduct)
    if sort_by in ['paged_price', 'paged_popularity', 'paged_name']:
        query = query.order_by(getattr(PagedProduct, sort_by).desc())
    if category:
        query = query.filter(PagedProduct.paged_category == category)
    if min_price:
        query = query.filter(PagedProduct.paged_price >= float(min_price))
    if max_price:
        query = query.filter(PagedProduct.paged_price <= float(max_price))
    total = query.count()
    products = query.offset((page-1)*page_size).limit(page_size).all()
    session.close()
    return total, products

def batch_add_paged_products(products):
    session = Session()
    objs = [PagedProduct(**p) for p in products]
    session.bulk_save_objects(objs)
    session.commit()
    session.close()
    return len(objs)

def batch_delete_paged_products(ids):
    session = Session()
    session.query(PagedProduct).filter(PagedProduct.paged_id.in_(ids)).delete(synchronize_session=False)
    session.commit()
    session.close()
    return len(ids)

def batch_update_paged_products(updates):
    session = Session()
    for upd in updates:
        session.query(PagedProduct).filter(PagedProduct.paged_id == upd['paged_id']).update(upd)
    session.commit()
    session.close()
    return len(updates)
