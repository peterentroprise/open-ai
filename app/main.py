from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline, set_seed

app = FastAPI()

origins = [
    "https://entroprise.com/",
    "https://www.entroprise.com/",
    "http://entroprise.com/",
    "http://entroprise.com",
    "http://localhost/",
    "http://localhost:8000/",
    "http://127.0.0.1:8000/",
    "http://127.0.0.1/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    text: str
    seed: int = 32
    max_length: int = 300
    num_return_sequences: int = 1


MODEL_PATH = "/ml-models/gpt2"
generator = pipeline("text-generation", model=MODEL_PATH)


@app.get("/")
def read_root():
    return {"Hello": "Universe"}


@app.post("/generate/")
def generate_text(item: Item):
    set_seed(item.seed)
    return generator(item.text, max_length=item.max_length, num_return_sequences=item.num_return_sequences)
