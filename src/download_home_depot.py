from huggingface_hub import hf_hub_download

def download_home_depot():
    destino = "data/raw/home_depot"

    hf_hub_download(
        repo_id="bstds/home_depot",
        repo_type="dataset",
        filename="data/train-00000-of-00001-9de242b7603049c1.parquet",
        local_dir=destino,
    )

if __name__ == "__main__":
    download_home_depot()
