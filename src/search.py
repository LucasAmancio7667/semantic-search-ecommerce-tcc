from elasticsearch import Elasticsearch


def search(index_name, query_text, tamanho=10):
    es = Elasticsearch("http://localhost:9200")

    query = {
        "multi_match": {
            "query": query_text,
            "fields": ["title", "description"],
        }
    }

    resultado = es.search(index=index_name, query=query, size=tamanho)
    return resultado["hits"]["hits"]