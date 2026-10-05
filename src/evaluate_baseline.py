import math
import pandas as pd
from src.search import search

KS = [5, 10, 15, 25, 50]


def dcg_at_k(relevancias, k):
    return sum(rel / math.log2(i + 1) for i, rel in enumerate(relevancias[:k], start=1))


def ndcg_at_k(y_true, y_score, k):
    ordenado = sorted(zip(y_score, y_true), reverse=True)
    relevancias_no_ranking = [rel for _, rel in ordenado]

    dcg = dcg_at_k(relevancias_no_ranking, k)
    idcg = dcg_at_k(sorted(y_true, reverse=True), k)

    return dcg / idcg if idcg > 0 else 0.0


def evaluate_baseline():
    queries = pd.read_csv("data/raw/wands/query.csv", sep="\t")
    labels = pd.read_csv("data/raw/wands/label.csv", sep="\t")

    relevancia = {"Exact": 2, "Partial": 1, "Irrelevant": 0}
    labels["relevancia"] = labels["label"].map(relevancia)

    scores_por_k = {k: [] for k in KS}

    for _, q in queries.iterrows():
        resultados = search("wands", q["query"], tamanho=max(KS))
        if not resultados:
            continue

        julgamentos = labels[labels["query_id"] == q["query_id"]].groupby("product_id")["relevancia"].max()

        y_true = [int(julgamentos.get(r["_source"]["id"], 0)) for r in resultados]
        y_score = [r["_score"] for r in resultados]

        for k in KS:
            scores_por_k[k].append(ndcg_at_k(y_true, y_score, k))

    return {k: sum(scores) / len(scores) for k, scores in scores_por_k.items()}


if __name__ == "__main__":
    resultados = evaluate_baseline()
    for k, valor in resultados.items():
        print(f"nDCG@{k} baseline (BM25/WANDS): {valor:.4f}")