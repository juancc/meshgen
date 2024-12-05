"""
Download models and load generator

JCA
"""

from huggingface_hub import hf_hub_download

import meshgen.globals as gb

def download_models(model_dir):
    print(f"Downloading model: {gb.MANIFEST['repo_id']}:{gb.MANIFEST['filename']}")
    hf_hub_download(gb.MANIFEST["repo_id"], filename=gb.MANIFEST["filename"], local_dir=model_dir)


if __name__ == '__main__':
    download_models('.')