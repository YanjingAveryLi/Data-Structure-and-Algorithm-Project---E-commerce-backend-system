from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ORM模型：磁盘存储用
class PagedProduct(Base):
    __tablename__ = 'paged_products'
    paged_id = Column(String, primary_key=True)
    paged_name = Column(String, index=True)
    paged_category = Column(String, index=True)
    paged_price = Column(Float, index=True)
    paged_popularity = Column(Integer, index=True)
    paged_stock = Column(Integer)
    paged_status = Column(String)
    paged_sales = Column(Integer)
    paged_rating = Column(Float)
    paged_description = Column(String)
    paged_image_url = Column(String)

    def to_dict(self):
        return {
            'paged_id': self.paged_id,
            'paged_name': self.paged_name,
            'paged_category': self.paged_category,
            'paged_price': self.paged_price,
            'paged_popularity': self.paged_popularity,
            'paged_stock': self.paged_stock,
            'paged_status': self.paged_status,
            'paged_sales': self.paged_sales,
            'paged_rating': self.paged_rating,
            'paged_description': self.paged_description,
            'paged_image_url': self.paged_image_url
        }

# dataclass模型：内存/算法/数据生成用   
@dataclass
class Product:
    id: str
    name: str
    brand: str
    category: str
    price: float
    popularity: int
    stock: int
    status: str
    sales: int
    rating: float
    description: str
    image_url: str
    created_date: str

    def __repr__(self):
        return (f"Product({self.id}, {self.name}, {self.brand}, {self.category}, "
                f"${self.price}, 热度:{self.popularity}, 库存:{self.stock}, "
                f"状态:{self.status}, 销量:{self.sales}, 评分:{self.rating}, "
                f"创建:{self.created_date})")
    
@dataclass
class Customer:
    def __init__(self, id, name, type, purchase_power, activity_level, join_date,
                 gender=None, age=None, phone=None, email=None, region=None, score=0):
        self.id = id
        self.name = name
        self.type = type
        self.purchase_power = purchase_power
        self.activity_level = activity_level
        self.join_date = join_date
        self.gender = gender
        self.age = age
        self.phone = phone
        self.email = email
        self.region = region
        self.score = score

@dataclass
class CustomerRelation:
    from_customer: str
    to_customer: str
    weight: float
    relation_type: str

    def __repr__(self):
        return f"Relation({self.from_customer} -> {self.to_customer}, 权重:{self.weight})"

@dataclass
class MarketingTask:
    id: str
    name: str
    type: str
    urgency: float
    influence: float
    priority: float
    created_date: str
    status: str = "Pending"  # Pending, In Progress, Completed
    assigned_to: Optional[str] = None

    def __repr__(self):
        return f"Task({self.id}, {self.name}, 优先级:{self.priority})"