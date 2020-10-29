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

class SumItem(BaseModel):
    text: str
    min_length: int = 10
    max_length: int = 100



GEN_MODEL_PATH = "/ml-models/gpt2"

SUM_MODEL_PATH = "/ml-models/facebookbart-large-cnn"

generator = pipeline("text-generation", model=GEN_MODEL_PATH)

summarizer = pipeline("summarization", model=SUM_MODEL_PATH, tokenizer=SUM_MODEL_PATH)


@app.get("/")
def read_root():
    return {"Hello": "Universe"}

@app.post("/generate/")
def generate_text(item: Item):
    set_seed(item.seed)
    return generator(item.text, max_length=item.max_length, num_return_sequences=item.num_return_sequences)

@app.post("/summarize/")
def summarize_text(item: SumItem):
    return summarizer(item.text, min_length=item.min_length, max_length=item.max_length)
