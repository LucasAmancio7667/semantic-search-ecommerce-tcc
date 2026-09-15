import pandas as pd
from sklearn.metrics import ndcg_score
from src.search import search

K = 10


def evaluate_baseline():
    queries = pd.read_csv("data/raw/wands/query.csv", sep="\t")
    labels = pd.read_csv("data/raw/wands/label.csv", sep="\t")

    relevancia = {"Exact": 2, "Partial": 1, "Irrelevant": 0}
    labels["relevancia"] = labels["label"].map(relevancia)

    scores_ndcg = []

    for _, q in queries.iterrows():
        resultados = search("wands", q["query"], tamanho=K)
        if not resultados:
            continue

        julgamentos = labels[labels["query_id"] == q["query_id"]].groupby("product_id")["relevancia"].max()

        y_true = [int(julgamentos.get(r["_source"]["id"], 0)) for r in resultados]
        y_score = [r["_score"] for r in resultados]

        scores_ndcg.append(ndcg_score([y_true], [y_score], k=K))

    return sum(scores_ndcg) / len(scores_ndcg)


if __name__ == "__main__":
    print(f"nDCG@{K} baseline (BM25/WANDS): {evaluate_baseline():.4f}")