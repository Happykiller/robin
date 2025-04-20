# apis\seed.py
import json
import requests

GRAPHQL_URL = "http://localhost:8000/graphql"

def load_products(filepath: str):
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)

def send_create_product(product: dict):
    query = """
        mutation createProduct($product: ProductInput!) {
            createProduct(product: $product)
        }
    """
    payload = {
        "query": query,
        "variables": { "product": product }
    }

    response = requests.post(GRAPHQL_URL, json=payload)
    if response.ok:
        data = response.json()
        if "errors" in data:
            print(f"❌ Error for {product['code']}: {data['errors']}")
        else:
            print(f"✔ Created: {product['code']}")
    else:
        print(f"🚨 HTTP error for {product['code']}: {response.status_code}")

if __name__ == "__main__":
    products = load_products("../docs/seeds/products.json")
    for product in products:
        send_create_product(product)
