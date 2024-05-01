import typer
from llama_cpp import Llama

app = typer.Typer()

PROMPT = """<|system|>
You're a nice chatbot
<|end|>
<|user|>
{msg}
<|end|>
<|assistant|>
"""

stop = ["<|system|>", "<|user|>", "<|assistant|>", "<|end|>"]

@app.command()
def main(model_path: str, msg: str = "Write a poem"):
    llama = Llama(model_path=model_path, n_threads=8, use_mlock=True, n_gpu_layers=0)
    print("Model loaded")
    print("Reponse:")
    print("--------")
    prompt = llama.tokenize(PROMPT.format(msg=msg).encode())
    for tok in llama.generate(prompt):
        print(llama.detokenize([tok]).decode(), sep="", end="", flush=True)



if __name__ == "__main__":
    app()



