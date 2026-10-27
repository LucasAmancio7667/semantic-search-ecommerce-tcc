# Estado da Arte — Trabalhos Relacionados

Tabela de classificação dos trabalhos relacionados ao TCC "Otimização de Busca Semântica
em E-commerce com Geração de Dados Sintéticos".

## Critérios de busca

- Fontes: Google Scholar, arXiv, BDTD/CAPES (teses e dissertações nacionais)
- Termos: "semantic product search", "e-commerce embedding retrieval", "synthetic query
  generation LLM", "retrieve and rerank e-commerce"

## Matriz de comparação

| Trabalho | Dataset | Arquitetura / Ranqueamento | LLM(s) usado(s) | Modelo de Embedding | Domínio | Métrica (valor, dataset) | Gap / Limitação |
|---|---|---|---|---|---|---|---|
| Silva, L. (2023) — DAPDR | NTCIR, ACORDAR | Retrievers densos fine-tunados (sem filtro léxico BM25 antes) | docTTTTTquery (T5 gerador de queries sintéticas) | DPR, BERT, SBERT e MPNET (comparados em versão original vs. fine-tunada); SBERT também usado para medir similaridade na filtragem de dados | Busca de datasets acadêmicos/governamentais (não e-commerce) | nDCG@k, comparando modelo original (O) vs fine-tunado (F) | Domínio diferente (não e-commerce); não usa retrieve-and-rerank com BM25; não compara SLM local vs LLM de API |
| Burtscher, L. (2024) | TREC Product Search dataset (baseado no ESCI) | Two-tower (dual-encoder) | BART (Bidirectional and Auto-Regressive Transformer) | GTE | E-commerce (busca de produtos) | nDCG@10 como métrica principal | Compara BM25 e two-tower como alternativas concorrentes, sem combiná-los em retrieve-and-rerank; usa um único gerador (BART) fine-tunado especificamente para a tarefa, sem comparar múltiplos LLMs/SLMs generalistas via prompting — não explora a distinção local (SLM) vs. API (LLM) que é a contribuição original deste TCC. |
| Christakopoulou, Patel, Velaga, Gaikwad, Suchter & Sundaranatha (2026) — App Store Search (Apple) | Logs históricos de busca da App Store (milhões de pares query-app, relevância comportamental) + conjunto menor de julgamentos textuais de juízes humanos (fine-tuning/validação do LLM-juiz) — proprietário, não público | Ranker de produção multiobjetivo, combinando rótulos comportamentais e textuais via *scalarization* (mistura ponderada dos dados de treino, proporção como hiperparâmetro ajustável — ex. 90-10, 70-30, 50-50) para navegar a fronteira de Pareto | Três configurações in-house comparadas: Pretrained 3B, Pretrained 30B, Finetuned 3B — o FT-3B (fine-tunado nos julgamentos humanos) supera o PT-30B mesmo sendo 10x menor (arquitetura/família não divulgada, só o tamanho) | Não mencionado/não aplicável | Busca comercial — App Store (marketplace de apps, não e-commerce físico) | Precision/Recall/F1 (qualidade do LLM-juiz); NDCG@1,3,7 textual e comportamental (impacto no ranker); A/B test mundial — conversão +0,24% (significativo, vencendo em 89% das lojas), maior ganho em *tail queries* | Não revela a arquitetura/família dos LLMs, só o tamanho; detalhes de prompt design omitidos "por brevidade"; avaliação restrita à App Store, sem discutir generalização pra outros domínios; gera **labels de relevância** pra treinar um ranker supervisionado, diferente das **consultas sintéticas** pra calibrar embedding usadas neste TCC |



| Query2doc (2023) | *a preencher* | *a preencher* | *a preencher* | *a preencher* | *a preencher* | *a preencher* | *a preencher* |
| *(próximos trabalhos)* | | | | | | | |
