"""
Load LLM model and generate mesh

JCA
"""
import llama_cpp


def generate(model_path):

    llm = llama_cpp.Llama(
        model_path=f'{model_path}/LLaMA-Mesh-Q4_K_M.gguf',
        n_gpu_layers=-1,
        seed=1337,
        n_ctx=4096,
        )
    

    prompt = 'generate the 3d mesh of a chair.'

    messages = [
                {"role": "system", "content": "You are a helpful assistant that can generate 3D obj files."},
                {"role": "user", "content": prompt}
            ]

    temperature = 0.9


    line_buffer = ''
    text = ''

    with open("test.txt", "a") as myfile:
        for chunk in llm.create_chat_completion(
                            messages=messages,
                            stream=True,
                            temperature=temperature
                        ):
            delta = chunk["choices"][0]["delta"]
            if "content" not in delta:
                continue
            content = delta["content"]
        myfile.write(content + ' ')



if __name__ == '__main__':
    generate('/Users/jarbel16/Library/Mobile Documents/com~apple~CloudDocs/Data/GenerativeDesign/LLama-mesh/')