import requests
from pathlib import Path

def download_wands():
    base_url = "https://raw.githubusercontent.com/wayfair/WANDS/main/dataset"
    files = ["product.csv", "query.csv", "label.csv"]
    destino = Path("data/raw/wands")
    destino.mkdir(parents=True, exist_ok=True)

    for nome_arquivo in files:
        resposta = requests.get(f"{base_url}/{nome_arquivo}")
        (destino / nome_arquivo).write_bytes(resposta.content)
        print(f"Baixado: {nome_arquivo}")

if __name__ == "__main__":
    download_wands()