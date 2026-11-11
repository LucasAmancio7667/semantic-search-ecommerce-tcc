import os
import time

import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

from src.few_shot_examples import SYSTEM_PROMPT, build_messages, FEW_SHOT_PRODUCT_IDS

load_dotenv()

MODELO = "claude-haiku-5-5"
TAMANHO_AMOSTRA = 50
SEED = 42


def gerar_query_sintetica(cliente, title, description):
    resposta = cliente.messages.create(
        model=MODELO,
        max_tokens=30,
        system=SYSTEM_PROMPT,
        messages=build_messages(title, description),
    )
    texto = next(bloco.text for bloco in resposta.content if bloco.type == "text")
    return texto.strip()


def gerar_amostra_wands():
    cliente = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    produtos = pd.read_csv("data/raw/wands/product.csv", sep="\t").fillna("")
    produtos = produtos[~produtos["product_id"].isin(FEW_SHOT_PRODUCT_IDS)]
    amostra = produtos.sample(TAMANHO_AMOSTRA, random_state=SEED)

    resultados = []
    for _, produto in amostra.iterrows():
        query_sintetica = gerar_query_sintetica(
            cliente, produto["product_name"], produto["product_description"]
        )
        resultados.append({
            "product_id": produto["product_id"],
            "title": produto["product_name"],
            "query_sintetica": query_sintetica,
        })
        print(f"{produto['product_name'][:50]:<50} -> {query_sintetica}")
        time.sleep(0.5)  # evita rajada de requisições

    df = pd.DataFrame(resultados)
    os.makedirs("data/synthetic", exist_ok=True)
    df.to_csv("data/synthetic/wands_queries_claude_sample.csv", index=False)
    print(f"\n{len(df)} queries sintéticas salvas em data/synthetic/wands_queries_claude_sample.csv")


if __name__ == "__main__":
    gerar_amostra_wands()
