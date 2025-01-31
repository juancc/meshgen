"""
Auxiliary function

JCA
"""
import os

from huggingface_hub import hf_hub_download
import meshgen.globals as gb


def setup_jupyter():
    """Setup Jupyter notebook (Google Colab)"""
    os.system('pip install llama_cpp_python==0.2.90 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121')
    os.system('pip install open3d')
    os.system('pip install huggingface_hub')


def download_model(quality, save_path):
    """download model from Huggingface Hub"""
    model_name = gb.MODELS[quality]
    manifest =  {
            "repo_id": "bartowski/LLaMA-Mesh-GGUF",
            "filename": model_name,
        }
    print(f"Downloading model: {manifest['repo_id']}:{manifest['filename']}")
    hf_hub_download(manifest["repo_id"], filename=manifest["filename"], local_dir=save_path)

