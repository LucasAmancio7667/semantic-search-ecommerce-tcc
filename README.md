# semantic-search-ecommerce-tcc

Trabalho de Conclusão de Curso: **Otimização de Busca Semântica em E-commerce com
Geração de Dados Sintéticos**.

Investiga uma arquitetura de recuperação em duas etapas (*retrieve-and-rerank*) para
busca de produtos em e-commerce: recuperação lexical inicial via BM25 (Elasticsearch),
seguida de reranking semântico por embeddings (SBERT), com geração de queries sintéticas
via LLMs/SLMs para calibração futura dos modelos de embedding.

## Arquitetura

1. **Recuperação lexical (BM25)** — busca `multi_match` padrão do Elasticsearch sobre
   título e descrição do produto.
2. **Reranking semântico (embeddings)** — busca por similaridade de cosseno (`knn`) usando
   embeddings gerados por modelos da família SBERT `all-*`
   (`all-MiniLM-L6-v2`, `all-MiniLM-L12-v2`, `all-mpnet-base-v2`, `all-distilroberta-v1`).
3. **Geração de dados sintéticos** (próxima fase) — queries sintéticas geradas por LLMs
   locais (SLMs) e de API, comparadas quanto ao ganho que produzem no fine-tuning dos
   embeddings.

## Datasets

| Dataset | Produtos | Queries | Status |
|---|---|---|---|
| [WANDS](https://github.com/wayfair/WANDS) (Wayfair) | 42.994 | ~480 | Baseline completo |
| [Home Depot Product Search Relevance](https://huggingface.co/datasets/bstds/home_depot) | 54.667 | 11.795 | Baseline em andamento |
| [TREC Product Search Track 2023](https://huggingface.co/datasets/trec-product-search/product-search-corpus) | 1.661.907 | — | Pendente (aguardando expansão de disco) |

Resultados detalhados em [`docs/resultados-baseline.md`](docs/resultados-baseline.md).

## Estrutura do repositório

```
src/
  download_wands.py          # baixa o dataset WANDS
  download_trec.py           # baixa o dataset TREC
  download_home_depot.py     # baixa o dataset Home Depot
  standardize.py             # padroniza cada dataset pro schema comum (id/title/description/source)
  create_index.py            # cria um índice no Elasticsearch
  index_documents.py         # indexa documentos (bulk)
  add_embeddings.py          # gera e indexa embeddings SBERT num campo dense_vector
  search.py                  # busca lexical (BM25 / multi_match)
  search_semantico.py        # busca semântica (knn)
  evaluate_baseline.py                       # avaliação nDCG — BM25 / WANDS
  evaluate_baseline_semantico.py             # avaliação nDCG — semântico / WANDS
  evaluate_baseline_home_depot.py            # avaliação nDCG — BM25 / Home Depot
  evaluate_baseline_semantico_home_depot.py  # avaliação nDCG — semântico / Home Depot
docs/
  estado-da-arte/related-work.md   # trabalhos relacionados
  resultados-baseline.md           # resultados de avaliação (BM25 vs. semântico)
```

## Como rodar

Pré-requisitos: Python 3.11+, Elasticsearch 9.x rodando em `localhost:9200`.

```bash
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1 | Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

Baixar um dataset, criar o índice e indexar (exemplo com o WANDS):

```bash
python -m src.download_wands
python -c "from src.create_index import create_index; create_index('wands')"
python -c "from src.index_documents import index_documents; from src.standardize import standardize_wands; index_documents('wands', standardize_wands())"
```

Avaliar o baseline BM25:

```bash
python -m src.evaluate_baseline
```

## Status do projeto

Em desenvolvimento — orientação de Levy de Souza Silva (IFPE Campus Belo Jardim).
