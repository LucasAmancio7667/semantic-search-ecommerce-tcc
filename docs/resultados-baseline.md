# Resultados — Baseline BM25 vs. Reranking Semântico (WANDS)

Resultados da Fase 3 do projeto: comparação entre a recuperação lexical (BM25, via
Elasticsearch `multi_match`) e o reranking semântico por embeddings (Elasticsearch `knn`),
usando os quatro modelos oficiais da família SBERT `all-*`.

## Metodologia

- Dataset: WANDS (42.994 produtos, consultas e julgamentos de relevância Exact/Partial/Irrelevant)
- Métrica: nDCG, calculado nos cortes K = 5, 10, 15, 25, 50
- Baseline lexical: BM25 padrão do Elasticsearch sobre os campos `title` + `description`
- Baseline semântico: embedding de `title + description` gerado por cada modelo, busca por
  similaridade de cosseno (`knn`) no índice
- Modelos avaliados: `all-MiniLM-L6-v2` (384 dims), `all-MiniLM-L12-v2` (384 dims),
  `all-mpnet-base-v2` (768 dims), `all-distilroberta-v1` (768 dims)

## Resultados

| Modelo | nDCG@5 | nDCG@10 | nDCG@15 | nDCG@25 | nDCG@50 |
|---|---|---|---|---|---|
| BM25 (baseline lexical) | 0.6835 | 0.6800 | 0.6908 | 0.7187 | 0.8361 |
| all-MiniLM-L6-v2 | 0.7097 | 0.7129 | 0.7153 | 0.7366 | 0.8447 |
| all-MiniLM-L12-v2 | **0.7536** | **0.7552** | **0.7582** | **0.7765** | **0.8701** |
| all-mpnet-base-v2 | 0.7243 | 0.7257 | 0.7273 | 0.7479 | 0.8531 |
| all-distilroberta-v1 | 0.6312 | 0.6296 | 0.6413 | 0.6684 | 0.7871 |

## Discussão

- Três dos quatro modelos semânticos (MiniLM-L6, MiniLM-L12, MPNet) superam o baseline BM25
  em todos os cortes de nDCG, confirmando o ganho esperado do reranking por embeddings sobre
  a recuperação puramente lexical.
- O `all-MiniLM-L12-v2` foi o melhor modelo em todos os cortes, inclusive superando o
  `all-mpnet-base-v2` — maior em número de dimensões (768 vs. 384) e geralmente apontado
  como o mais forte da família `all-*` em benchmarks gerais de similaridade semântica. Isso
  sugere que, no domínio específico de busca de produtos de e-commerce, um modelo menor pode
  generalizar melhor do que um modelo maior otimizado para tarefas mais genéricas.
- O `all-distilroberta-v1` foi o único modelo em que o reranking semântico piora o resultado
  em relação ao BM25 em todos os cortes — é conhecido na literatura do SBERT como o mais
  fraco da família `all-*` para tarefas de similaridade semântica, o que se confirma aqui de
  forma consistente.

## Próximos passos

- Baseline BM25/semântico no dataset TREC Product Search 
- Geração de queries sintéticas via LLMs/SLMs para fine-tuning dos embeddings (contribuição
  original do TCC)
