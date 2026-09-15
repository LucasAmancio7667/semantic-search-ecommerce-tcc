from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def index_documents(index_name, documentos):
    es = Elasticsearch("http://localhost:9200")

    actions = (
        {"_index": index_name, "_id": doc["id"], "_source": doc}
        for doc in documentos
    )

    bulk(es, actions)