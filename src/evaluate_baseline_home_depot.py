import pandas as pd
from sklearn.metrics import ndcg_score
from src.search import search

KS = [5, 10, 15, 25, 50]


def evaluate_baseline_home_depot():
    df = pd.read_parquet("data/raw/home_depot/data/train-00000-of-00001-9de242b7603049c1.parquet")

    scores_por_k = {k: [] for k in KS}

    for query_text, grupo in df.groupby("query"):
        resultados = search("home_depot", query_text, tamanho=max(KS))
        if len(resultados) < 2:
            continue

        julgamentos = grupo.groupby("entity_id")["relevance"].max()

        y_true = [float(julgamentos.get(r["_source"]["id"], 0)) for r in resultados]
        y_score = [r["_score"] for r in resultados]

        for k in KS:
            scores_por_k[k].append(ndcg_score([y_true], [y_score], k=k))

    return {k: sum(scores) / len(scores) for k, scores in scores_por_k.items()}


if __name__ == "__main__":
    resultados = evaluate_baseline_home_depot()
    for k, valor in resultados.items():
        print(f"nDCG@{k} baseline (BM25/Home Depot): {valor:.4f}")
