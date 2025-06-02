from db import Session
from models import PagedProduct
from data_generator import DataGenerator

def import_paged_products(n=1000):
    session = Session()
    generator = DataGenerator()
    products = generator.generate_paged_products(n)
    objs = [PagedProduct(**p) for p in products]
    session.bulk_save_objects(objs)
    session.commit()
    session.close()
    print(f"已导入 {len(objs)} 条商品到 paged_products 表")

if __name__ == "__main__":
    import_paged_products(1000)
