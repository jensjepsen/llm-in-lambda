import fastapi, pydantic, typing, json, logging
from llama_cpp import Llama

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models
class Message(pydantic.BaseModel):
    content: str
    role: typing.Literal["user", "assistant", "system"]
    
    def __str__(self):
        return f"<|{self.role}|>\n{self.content}\n<|end|>"


# FastAPI app
app = fastapi.FastAPI()

# Load the model
llama = Llama(model_path=".models/Phi-3-mini-4k-instruct-q4.gguf", n_threads=6, n_gpu_layers=0, n_ctx=2048)

# Helpers
def messages_to_prompt(messages):
    return "\n".join(map(str, messages)) + "\n<|assistant|>"

def stream_response(messages: typing.List[Message]):
    prompt = messages_to_prompt(messages)
    for resp in llama(
        prompt=prompt,
        stream=True,
        stop=["<|system|>", "<|user|>", "<|assistant|>", "<|end|>"],
        max_tokens=None,
    ):
        yield "event: responsePart\ndata: " + json.dumps(resp) + "\n\n"

# Routes
@app.post("/chat")
async def chat(messages: typing.List[Message]):
    return fastapi.responses.StreamingResponse(stream_response(messages), media_type="text/event-stream")

@app.get("/hello-world")
async def hello_world():
    return fastapi.responses.StreamingResponse(stream_response([Message(content="Hello!", role="user")]), media_type="text/event-stream")