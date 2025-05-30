# main.py
import logging
import strawberry
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter

from services.i18n.translation import TranslationService
from services.db.memory import InMemoryProductRepository
from services.embeddings.labse_embedder import EmbeddingService
from exposers.resolvers.product import ProductQuery, ProductMutation

repository = InMemoryProductRepository()
embedder = EmbeddingService()
translator = TranslationService()

logging.basicConfig(level=logging.INFO)

@strawberry.type
class Query(ProductQuery):
    @strawberry.field
    def hello(self) -> str:
        return "Hello, GraphQL ✨"

@strawberry.type
class Mutation(ProductMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)

async def get_context(request: Request):
    return {
        "repository": repository,
        "embedder": embedder,
        "translator": translator
    }

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")