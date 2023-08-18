import sys

sys.path.append("../..")
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base, engine


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    stock = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

    article_product_detail = relationship("ProductDetail", back_populates="product_detail_article")


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

    product_product_detail = relationship("ProductDetail", back_populates="product_detail_product")


class ProductDetail(Base):
    __tablename__ = "product_detail"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    article_id = Column(Integer, ForeignKey("article.id"))
    amount_of = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

    product_detail_product = relationship("Product", back_populates="product_product_detail")
    product_detail_article = relationship("Article", back_populates="article_product_detail")


Base.metadata.create_all(bind=engine)
