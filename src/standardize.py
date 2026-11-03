import gzip
import json
import pandas as pd


def standardize_wands():
    df = pd.read_csv("data/raw/wands/product.csv", sep="\t").fillna("")

    for _, row in df.iterrows():
        description = f"{row['product_description']} {row['product_features']}".strip()
        yield {
            "id": row["product_id"],
            "title": row["product_name"],
            "description": description,
            "source": "wands",
        }


def standardize_trec():
    with gzip.open("data/raw/trec/corpus.jsonl.gz", "rt") as f:
        for linha in f:
            doc = json.loads(linha)
            yield {
                "id": doc["docid"],
                "title": doc["title"],
                "description": doc["text"],
                "source": "trec",
            }


def standardize_home_depot():
    df = pd.read_parquet("data/raw/home_depot/data/train-00000-of-00001-9de242b7603049c1.parquet")
    df = df.drop_duplicates(subset="entity_id").fillna("")

    for _, row in df.iterrows():
        yield {
            "id": row["entity_id"],
            "title": row["name"],
            "description": row["description"],
            "source": "home_depot",
        }
