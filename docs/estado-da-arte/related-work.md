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
| Silva, L. (2023) — DAPDR | NTCIR, ACORDAR | Retrievers densos fine-tunados (sem filtro léxico BM25 antes) | docTTTTTquery (T5 gerador de queries sintéticas) | *a revisar* | Busca de datasets acadêmicos/governamentais (não e-commerce) | nDCG@k, comparando modelo original (O) vs fine-tunado (F) | Domínio diferente (não e-commerce); não usa retrieve-and-rerank com BM25; não compara SLM local vs LLM de API |
| Burtscher, L. (2024)  |  | TREC Product Search dataset ESCI | two-tower (dual-encoder) | BART (Bidirectional and Auto-Regressive Transformer) | GTE | E-commerce (busca de produtos) | E-commerce (busca de produtos) |
nDCG@10 como métrica principal | Compara BM25 e two-tower como alternativas concorrentes, sem combiná-los em retrieve-and-rerank; usa um único gerador (BART) fine-tunado especificamente para a tarefa, sem comparar múltiplos LLMs/SLMs generalistas via prompting — não explora a distinção local (SLM) vs. API (LLM) que é a contribuição original deste TCC. |



| Query2doc (2023) | *a preencher* | *a preencher* | *a preencher* | *a preencher* | *a preencher* | *a preencher* | *a preencher* |
| *(próximos trabalhos)* | | | | | | | |
