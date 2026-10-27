from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def add_embeddings(index_name, documentos, modelo_nome, campo_embedding, dims):
    es = Elasticsearch("http://localhost:9200")

    es.indices.put_mapping(
        index=index_name,
        properties={campo_embedding: {"type": "dense_vector", "dims": dims, "similarity": "cosine"}},
    )

    modelo = SentenceTransformer(modelo_nome)
    documentos = list(documentos)

    textos = [f"{doc['title']} {doc['description']}" for doc in documentos]
    vetores = modelo.encode(textos, batch_size=32, show_progress_bar=True)

    actions = (
        {"_op_type": "update", "_index": index_name, "_id": doc["id"], "doc": {campo_embedding: vetor.tolist()}}
        for doc, vetor in zip(documentos, vetores)
    )

    bulk(es, actions)