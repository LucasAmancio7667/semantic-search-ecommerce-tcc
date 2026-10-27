from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

_modelos_carregados = {}


def search_semantico(index_name, query_text, modelo_nome, campo_embedding, k=10):
    es = Elasticsearch("http://localhost:9200")

    if modelo_nome not in _modelos_carregados:
        _modelos_carregados[modelo_nome] = SentenceTransformer(modelo_nome)
    modelo = _modelos_carregados[modelo_nome]

    vetor_da_query = modelo.encode(query_text).tolist()

    resultado = es.search(
    index=index_name,
    knn={
        "field": campo_embedding,
        "query_vector": vetor_da_query,
        "k": k,
        "num_candidates": 100,
    },
    size=k,
    )
    return resultado["hits"]["hits"]
