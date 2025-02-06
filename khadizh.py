from datetime import datetime
from typing import List, Optional

import strawberry
from sqlalchemy import Column, Float, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# === Определение модели товара ===
class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# === GraphQL Схема ===
@strawberry.type
class Product:
    id: int
    name: str
    description: str
    price: float
    created_at: datetime


@strawberry.type
class Query:
    @strawberry.field
    def get_products(self, min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[Product]:
        session = SessionLocal()
        query = session.query(ProductModel)

        if min_price is not None:
            query = query.filter(ProductModel.price >= min_price)
        if max_price is not None:
            query = query.filter(ProductModel.price <= max_price)

        products = query.all()
        session.close()
        return [Product(id=p.id, name=p.name, description=p.description, price=p.price, created_at=p.created_at) for p
                in products]

    @strawberry.field
    def get_product(self, id: int) -> Optional[Product]:
        session = SessionLocal()
        product = session.query(ProductModel).filter(ProductModel.id == id).first()
        session.close()
        if product:
            return Product(id=product.id, name=product.name, description=product.description, price=product.price,
                           created_at=product.created_at)
        return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(self, name: str, description: str, price: float) -> int:
        session = SessionLocal()
        new_product = ProductModel(name=name, description=description, price=price)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        session.close()
        return new_product.id


schema = strawberry.Schema(query=Query, mutation=Mutation)


from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
