# Geração de Queries Sintéticas — Claude (LLM via API)

Primeira fase da contribuição original do TCC: gerar queries sintéticas de busca a
partir da ficha de um produto (título + descrição), usando um LLM via API (Claude) com
prompt few-shot. Essas queries sintéticas servem como pares de treino adicionais
(query, produto) para o fine-tuning do modelo de embedding, complementando as queries
reais do WANDS/Home Depot. Fase posterior vai comparar esse resultado com queries
geradas por SLMs locais (Phi-4-mini, Qwen, Llama) rodando na GPU do IFPE.

## Metodologia

- Modelo: `claude-haiku-5-5` (via Anthropic API)
- Few-shot: 6 exemplos reais do WANDS, pares (produto, query) com label `Exact`
  (ou seja, julgados por humanos como correspondência perfeita produto-query),
  amostrados de `product_class` distintos (`random.seed(7)`) para cobrir diversidade de
  categorias de produto e evitar que o modelo aprenda um padrão de query enviesado por
  um tipo de produto só
- Esta fase (validação): amostra de 50 produtos aleatórios do WANDS (`random_state=42`),
  excluindo os 6 produtos usados como exemplo few-shot
- Código: `src/few_shot_examples.py` (prompt + exemplos) e
  `src/generate_synthetic_queries.py` (script de geração)

## Prompt utilizado

### System prompt

```
Você é um sistema que simula consultas de busca reais, feitas por clientes de e-commerce, a partir da ficha de um produto. O objetivo é gerar dados sintéticos de treino para um modelo de busca semântica (embedding fine-tuning).

Regras importantes, baseadas em como clientes reais buscam (não como um redator de SEO escreveria):
- Consultas de clientes reais são curtas (1 a 5 palavras), informais, e frequentemente NÃO repetem o título do produto literalmente.
- Às vezes a consulta foca em um único atributo marcante (cor, material, tema, marca mencionada na descrição) em vez de descrever o produto inteiro.
- Às vezes a consulta usa um termo aproximado/coloquial em vez do termo técnico exato usado na ficha do produto.
- NUNCA gere uma consulta que seja apenas uma cópia ou paráfrase óbvia do título.
- A consulta gerada deve ser SEMPRE em inglês, igual aos exemplos abaixo — independente do idioma destas instruções, porque o dataset de referência (WANDS) é em inglês.

Dado o título e a descrição de um produto, gere APENAS UMA consulta de busca plausível que um cliente real digitaria para encontrar esse produto. Responda só com a consulta, sem explicação.
```

### Exemplos few-shot (produto → query)

| Produto | Descrição (resumida) | Query (few-shot) |
|---|---|---|
| tenor 1 - light single geometric pendant | this 1-light geometric mini pendant helps you outfit your ceiling in french country style! its frame... | kelly clarkson light fixtures |
| brucie monthly write on calendar magnetic wall mounted dry erase board | birthday parties, soccer practice, weekly errands; you name it, our schedules are always filled with... | monthly calendar |
| 59'' x 22'' freestanding soaking fiberglass bathtub with faucet | this product was designed with sleek soft curves and a glossy black exterior finish. the tub has an ... | black freestanding tub with faucet |
| enyart 134'' wide reversible modular sofa & chaise with ottoman | dive yourself in this cloud-like comfort, stylish, versatile modular sectional which sets easily for... | sofa with ottoman |
| resin staverden castle peacock fountain | allow nature's proud peacock to transform your home or garden into a place of quiet contemplation wi... | peacock |
| drelan rocking chair | the triton rocking chair combines style and comfort with a handsome modern design. this beautiful ac... | leather chairs |

A API da Anthropic recebe esses exemplos como um histórico de conversa real
(mensagens alternadas `user`/`assistant`), não como texto colado num bloco só — é assim
que o few-shot funciona nativamente na API de mensagens, e funciona melhor que
simular isso em um único prompt de texto.

## Resultados — amostra de validação (50 produtos, WANDS)

| product_id | Produto | Query sintética gerada |
|---|---|---|
| 30008 | paddy daybed | kids bedroom daybed with storage |
| 25204 | tensabowl accessory | bowl accessory |
| 28436 | holmwith resin free standing umbrella base | umbrella stand heavy base |
| 6558 | gratiana southwestern aztec bohemian reversible quilt set | southwestern aztec quilt |
| 28661 | methuen 121 '' wide reversible modular sectional | modular sectional couch |
| 23047 | campeon natural coco non-slip outdoor door mat | coir doormat outdoor |
| 42638 | arzola 45.3 '' console table | console table with drawers |
| 25726 | orion 28.3 '' console table | small console table with drawers |
| 12613 | ashford 24 '' h x 16 '' w x 1/2 '' d molded classic wainscot wall panel | wainscoting panel |
| 23278 | kohler tailor large double basin stainless steel sink with etched stone insert | farmhouse double sink |
| 34202 | galiena glass l-shape desk | glass computer desk with keyboard drawer |
| 3026 | ayesha curry enamel on steel 22 oz . food storage container | bacon grease container |
| 13355 | ulu real kissable decorative square pillow cover & insert | throw pillow cover with insert |
| 36452 | aneka 8 '' dark granite table lamp | granite lamp with glass shade |
| 12356 | osya sham | velvet pillow sham |
| 6887 | luxury executive chair | ergonomic office chair with lumbar support |
| 7782 | datey 2-light spotlight | adjustable wall light |
| 6239 | christmas pine tree | artificial christmas tree |
| 2706 | yann antique console table | white console table |
| 22057 | siloam functional chaise lounge | velvet chaise lounge with storage |
| 21781 | keenes solid wood tv stand for tvs up to 65 '' | mid century tv stand |
| 3936 | ayesha curry 12 cup non-stick muffin pan | nonstick cupcake pan |
| 19579 | maile butterfly leaf rubberwood solid wood dining table | extendable dining table |
| 36712 | christmas curl tree | christmas tree decor |
| 3777 | caseyville organizer with wall baskets | mail sorter wall rack |
| 14449 | akeira counter height 42 '' iron sled dining table | glass top dining table |
| 36197 | goethe bar & counter swivel bar stool | swivel bar stool with leather seat |
| 25135 | ontonagon 3 piece rattan sectional seating group with cushions | wicker patio set |
| 28721 | portsmouth upholstered bed | tufted platform bed with headboard |
| 18990 | alsiddiqa upholstered parsons chair in gray | gray kid friendly dining chairs |
| 12990 | orean task chair | ergonomic office chair with wheels |
| 17238 | welcome 30 in . x 18 in . outdoor door mat | outdoor doormat welcome |
| 15137 | fox run brands non-stick linked loaf pan | non-stick bread pan |
| 5758 | pineapple 1-gang toggle light switch wall plate | light switch cover |
| 6396 | boley 41 '' wide top grain leather club chair | leather club chair with nailhead trim |
| 10876 | timmie kitchen heart anti-fatigue mat | cushioned kitchen rug |
| 40161 | cates 3 piece bistro set | outdoor bistro table set |
| 27952 | minimo floating shelf | walnut wall shelf |
| 18821 | cormier twin over twin bunk bed | bunk beds for kids |
| 16028 | annex traditional beveled accent mirror | bedroom mirror |
| 39776 | arsenault 46 '' console table | rustic console table |
| 4706 | alexandrea drafting chair | ergonomic office chair with wheels |
| 31226 | casey 7 piece comforter set | bedding set |
| 13041 | artificial real touch tulips floral arrangement in vase | fake tulips in vase |
| 26438 | monarch abode architectural 3-gang toggle light switch / rocker combination wall plate | triple light switch cover plate |
| 8241 | 3pcs patio bistro set with 2 folding chairs & table outdoor dining furniture w/ round textured tempered glass tabletop , rust-free steel frame , space saving for balcony , yard | bistro set outdoor |
| 5154 | abberville 15.31 '' bed frame | wooden full bed frame |
| 10265 | garst ombre tufted graphite area rug | gray tufted rug |
| 39405 | 20 pair shoe rack | shoe organizer for closet |
| 33849 | calacatta azul matte 23.62 '' x 23.62 '' porcelain marble look wall & floor tile | blue marble tile |

## Observações

- Nenhuma query saiu em português nesta rodada (problema corrigido: a primeira versão
  do prompt gerou uma query em português por engano, já que o prompt de sistema está em
  português — foi adicionada uma instrução explícita para a consulta gerada ser sempre em
  inglês, já que o dataset de referência (WANDS) é em inglês).
- Vários casos bons, onde o modelo inferiu o uso do produto em vez de descrevê-lo
  literalmente (ex.: "ayesha curry enamel on steel 22 oz. food storage container" ->
  "bacon grease container"), ou trocou um termo técnico por um termo coloquial (ex.:
  "timmie kitchen heart anti-fatigue mat" -> "cushioned kitchen rug") — alinhado com o
  objetivo do prompt.
- Alguns casos saíram mais descritivos/próximos de um padrão "SEO" do que de uma busca
  real de cliente (ex.: duas queries de mesa de console geraram "console table with
  drawers" / "small console table with drawers", bem parecidas com o próprio título).
  Possível ajuste futuro no prompt: reforçar ainda mais a preferência por consultas de
  1-3 palavras.

## Próximos passos

- Validar esta abordagem com o professor orientador antes de gerar para os datasets
  completos (WANDS + Home Depot, ~97 mil produtos)
- Se aprovado: gerar via Message Batches API (custo ~50% menor) para os dois datasets
  completos
- Gerar o equivalente usando SLMs locais (Phi-4-mini, Qwen, Llama) na GPU do IFPE, para
  a comparação LLM vs. SLM que é a contribuição original do TCC
