from elasticsearch import Elasticsearch

MAPPING = {
    "properties": {
        "id": {"type": "keyword"},
        "title": {"type": "text"},
        "description": {"type": "text"},
        "source": {"type": "keyword"},
    }
}

def create_index(index_name):
    es = Elasticsearch("http://localhost:9200")
    es.indices.create(index=index_name, mappings=MAPPING)