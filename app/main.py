from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, set_seed

app = FastAPI()


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
