# apis\main.py
from apis.schemas.product import Product, ProductInput, ProductTranslation
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

from apis.resolvers.product import ProductQuery, ProductMutation
from services.db.memory import InMemoryProductRepository
from usecases.product import create as creatr_usecase, list as list_usecase

# Instanciation unique du repo
repository = InMemoryProductRepository()

# Fusion des resolvers
@strawberry.type
class Query(ProductQuery): ...
@strawberry.type
class Mutation(ProductMutation): ...

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, context_getter=lambda _: {"repository": repository})
    
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")