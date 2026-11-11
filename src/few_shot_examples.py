# Exemplos few-shot usados no prompt de geração de queries sintéticas.
# Selecionados do WANDS: pares (produto, query) com label "Exact", amostrados de
# product_class distintos (random.seed(7)) para cobrir diversidade de categorias.
# product_id listado aqui para excluir esses produtos da amostra de geração.

FEW_SHOT_EXAMPLES = [
    {
        "product_id": 4640,
        "title": "tenor 1 - light single geometric pendant",
        "description": (
            "this 1-light geometric mini pendant helps you outfit your ceiling in "
            "french country style! its frame is made from metal, and showcases an "
            "open cage-shaped silhouette with a horizontal scalloped ring that's "
            "surrounded by angled metal bars."
        ),
        "query": "kelly clarkson light fixtures",
    },
    {
        "product_id": 37302,
        "title": "brucie monthly write on calendar magnetic wall mounted dry erase board",
        "description": (
            "birthday parties, soccer practice, weekly errands; you name it, our "
            "schedules are always filled with something. here to help, this "
            "magnetic dry erase board keeps track of to-dos for the entire month."
        ),
        "query": "monthly calendar",
    },
    {
        "product_id": 33393,
        "title": "59'' x 22'' freestanding soaking fiberglass bathtub with faucet",
        "description": (
            "this product was designed with sleek soft curves and a glossy black "
            "exterior finish. the tub has an internal drain and can hold up to 55 "
            "gallons of water."
        ),
        "query": "black freestanding tub with faucet",
    },
    {
        "product_id": 1700,
        "title": "enyart 134'' wide reversible modular sofa & chaise with ottoman",
        "description": (
            "dive yourself in this cloud-like comfort, stylish, versatile modular "
            "sectional which sets easily for a variety of custom configurations. "
            "this relaxed silhouette has a large armrest and deep seat for great "
            "comfort."
        ),
        "query": "sofa with ottoman",
    },
    {
        "product_id": 36546,
        "title": "resin staverden castle peacock fountain",
        "description": (
            "allow nature's proud peacock to transform your home or garden into a "
            "place of quiet contemplation with its lilting water music surrounded "
            "by a cascade of feathers."
        ),
        "query": "peacock",
    },
    {
        "product_id": 39086,
        "title": "drelan rocking chair",
        "description": (
            "the triton rocking chair combines style and comfort with a handsome "
            "modern design. this beautiful accent chair has a walnut frame and is "
            "upholstered in a rich pu with nailhead trim creating a vintage look."
        ),
        "query": "leather chairs",
    },
]

SYSTEM_PROMPT = """Você é um sistema que simula consultas de busca reais, feitas por clientes de \
e-commerce, a partir da ficha de um produto. O objetivo é gerar dados sintéticos de \
treino para um modelo de busca semântica (embedding fine-tuning).

Regras importantes, baseadas em como clientes reais buscam (não como um redator de SEO \
escreveria):
- Consultas de clientes reais são curtas (1 a 5 palavras), informais, e frequentemente \
NÃO repetem o título do produto literalmente.
- Às vezes a consulta foca em um único atributo marcante (cor, material, tema, marca \
mencionada na descrição) em vez de descrever o produto inteiro.
- Às vezes a consulta usa um termo aproximado/coloquial em vez do termo técnico exato \
usado na ficha do produto.
- NUNCA gere uma consulta que seja apenas uma cópia ou paráfrase óbvia do título.
- A consulta gerada deve ser SEMPRE em inglês, igual aos exemplos abaixo — independente do idioma destas instruções, porque o dataset de referência (WANDS) é em inglês.

Dado o título e a descrição de um produto, gere APENAS UMA consulta de busca plausível \
que um cliente real digitaria para encontrar esse produto. Responda só com a consulta, \
sem explicação."""


def build_messages(title, description):
    """Monta a lista de mensagens (few-shot + produto alvo) para a API da Anthropic."""
    messages = []
    for exemplo in FEW_SHOT_EXAMPLES:
        messages.append({
            "role": "user",
            "content": f"Produto: {exemplo['title']}\nDescrição: {exemplo['description']}",
        })
        messages.append({"role": "assistant", "content": exemplo["query"]})

    messages.append({
        "role": "user",
        "content": f"Produto: {title}\nDescrição: {description}",
    })
    return messages


FEW_SHOT_PRODUCT_IDS = {e["product_id"] for e in FEW_SHOT_EXAMPLES}
