from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

# Define Category model
class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)

    # Relationship to Product
    products = relationship("Product", back_populates="category")

# Define Product model
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

    # Relationship to Category
    category = relationship("Category", back_populates="products")

# Create SQLite engine and session
engine = create_engine('sqlite:///shop.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Populate tables with sample data (if not already populated)
if session.query(Category).count() == 0:
    # Add categories
    electronics = Category(category_name='Electronics')
    groceries = Category(category_name='Groceries')
    session.add_all([electronics, groceries])
    session.commit()

    # Add products
    products = [
        Product(product_name='Smartphone', price=15000, category_id=electronics.category_id),
        Product(product_name='Laptop', price=50000, category_id=electronics.category_id),
        Product(product_name='Apples', price=100, category_id=groceries.category_id),
        Product(product_name='Bread', price=80, category_id=groceries.category_id)
    ]
    session.add_all(products)
    session.commit()

# Retrieve and print products with category info
all_products = session.query(Product).join(Category).all()
for product in all_products:
    print(f"Product: {product.product_name}, Price: Rs.{product.price:.2f}, Category: {product.category.category_name}")
