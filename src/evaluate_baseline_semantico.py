import pandas as pd
from sklearn.metrics import ndcg_score
from src.search_semantico import search_semantico

KS = [5, 10, 15, 25, 50]

MODELO_NOME = "all-distilroberta-v1"
CAMPO_EMBEDDING = "embedding_distilroberta"


def evaluate_baseline_semantico():
    queries = pd.read_csv("data/raw/wands/query.csv", sep="\t")
    labels = pd.read_csv("data/raw/wands/label.csv", sep="\t")

    relevancia = {"Exact": 2, "Partial": 1, "Irrelevant": 0}
    labels["relevancia"] = labels["label"].map(relevancia)

    scores_por_k = {k: [] for k in KS}

    for _, q in queries.iterrows():
        resultados = search_semantico(
            "wands", q["query"], MODELO_NOME, CAMPO_EMBEDDING, k=max(KS)
        )
        if not resultados:
            continue

        julgamentos = labels[labels["query_id"] == q["query_id"]].groupby("product_id")["relevancia"].max()

        y_true = [int(julgamentos.get(r["_source"]["id"], 0)) for r in resultados]
        y_score = [r["_score"] for r in resultados]

        for k in KS:
            scores_por_k[k].append(ndcg_score([y_true], [y_score], k=k))

    return {k: sum(scores) / len(scores) for k, scores in scores_por_k.items()}


if __name__ == "__main__":
    resultados = evaluate_baseline_semantico()
    for k, valor in resultados.items():
        print(f"nDCG@{k} semântico ({MODELO_NOME}/WANDS): {valor:.4f}")