from huggingface_hub import snapshot_download, hf_hub_download

def download_trec():
    destino = "data/raw/trec"

    snapshot_download(
        repo_id="trec-product-search/product-search-2023-queries",
        repo_type="dataset",
        local_dir=f"{destino}/queries",
    )
    snapshot_download(
        repo_id="trec-product-search/product-search-2023-qrels",
        repo_type="dataset",
        local_dir=f"{destino}/qrels",
    )
    hf_hub_download(
        repo_id="trec-product-search/product-search-corpus",
        repo_type="dataset",
        filename="corpus.jsonl.gz",
        local_dir=destino,
    )

if __name__ == "__main__":
    download_trec()