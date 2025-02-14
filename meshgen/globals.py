"""
Global variables

JCA
"""

MANIFEST = {
            "repo_id": "bartowski/LLaMA-Mesh-GGUF",
            "filename": "LLaMA-Mesh-Q4_K_M.gguf"
        }

# Mapping dict: quality: model name
MODELS = {
    'extremely': 'LLaMA-Mesh-Q6_K_L.gguf',
    'high': 'LLaMA-Mesh-Q6_K.gguf',
    'medium': 'LLaMA-Mesh-Q4_K_M.gguf',
    'low': 'LLaMA-Mesh-Q3_K_M.gguf',
    'debug':   'LLaMA-Mesh-Q2_K.gguf'
}