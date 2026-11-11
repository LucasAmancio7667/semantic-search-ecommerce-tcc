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

---

# Resultados — Baseline BM25 vs. Reranking Semântico (Home Depot)

Segundo dataset de validação, escolhido por ter uma escala semelhante ao WANDS
(diferente do TREC, grande demais para a VM compartilhada no momento).

## Metodologia

- Dataset: Home Depot Product Search Relevance (54.667 produtos únicos, 11.795 queries)
- Métrica: nDCG, calculado nos cortes K = 5, 10, 15, 25, 50
- Relevância: contínua (1.0 a 3.0, média de pelo menos 3 avaliações humanas por par
  query-produto) — diferente da relevância categórica (Exact/Partial/Irrelevant) do WANDS
- Baseline lexical: BM25 padrão do Elasticsearch sobre os campos `title` + `description`
- Baseline semântico: embedding de `title + description`, busca por similaridade de
  cosseno (`knn`) no índice
- Modelos avaliados: `all-MiniLM-L6-v2` (384 dims), `all-MiniLM-L12-v2` (384 dims),
  `all-mpnet-base-v2` (768 dims), `all-distilroberta-v1` (768 dims)

## Resultados

| Modelo | nDCG@5 | nDCG@10 | nDCG@15 | nDCG@25 | nDCG@50 |
|---|---|---|---|---|---|
| BM25 (baseline lexical) | **0.2900** | **0.3373** | **0.3720** | **0.4121** | **0.4610** |
| all-MiniLM-L12-v2 | 0.2741 | 0.3184 | 0.3511 | 0.3898 | 0.4370 |
| all-MiniLM-L6-v2 | 0.2548 | 0.2977 | 0.3293 | 0.3678 | 0.4148 |
| all-mpnet-base-v2 | 0.2523 | 0.2946 | 0.3268 | 0.3658 | 0.4124 |
| all-distilroberta-v1 | 0.2343 | 0.2751 | 0.3046 | 0.3395 | 0.3852 |

## Discussão

- Os valores absolutos de nDCG são bem mais baixos que no WANDS em todos os modelos —
  consistente com o Home Depot ser um dataset mais ruidoso, com queries curtas e
  coloquiais (termos de busca reais de usuários, nem sempre alinhados ao vocabulário do
  título/descrição do produto).
- Diferente do WANDS, aqui o BM25 supera **todos os quatro** modelos semânticos em todos
  os cortes de nDCG — um resultado oposto ao observado no primeiro dataset, onde o
  reranking semântico batia o BM25 já no modelo mais fraco (MiniLM-L6). Isso é o achado
  mais relevante dessa fase para a discussão do TCC: o ganho do reranking semântico sobre
  a recuperação lexical não é universal, parece depender de características do
  domínio/dataset (vocabulário, tamanho/estrutura das queries, ruído nos julgamentos de
  relevância).
- A ordem relativa entre os modelos semânticos se manteve parcialmente consistente com o
  WANDS: o MiniLM-L12 foi novamente o melhor dos quatro, e o DistilRoBERTa novamente o
  pior. A diferença foi entre MiniLM-L6 e MPNet, que ficaram praticamente empatados aqui
  (no WANDS o MPNet superava claramente o L6).
- Combinando os dois datasets, dá pra afirmar com mais confiança que o `all-MiniLM-L12-v2`
  é o modelo semântico mais robusto da família `all-*` para busca de produtos de
  e-commerce, e o `all-distilroberta-v1` o mais fraco, independente do dataset.

## Próximos passos

- Baseline BM25/semântico no dataset TREC Product Search (pendente de expansão de disco
  na VM compartilhada)
- Investigar por que o reranking semântico performa pior que o BM25 no Home Depot
  (hipóteses: queries muito curtas prejudicam a qualidade do embedding da query; ruído
  nos julgamentos de relevância; vocabulário muito específico do domínio "home
  improvement" pouco representado no pré-treino dos modelos `all-*`, que são de propósito
  geral)
- Geração de queries sintéticas via LLMs/SLMs para fine-tuning dos embeddings
  (contribuição original do TCC)
