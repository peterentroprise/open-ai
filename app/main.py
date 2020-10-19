from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, set_seed

app = FastAPI()

class Item(BaseModel):
    text: str

MODEL_PATH = "gpt2"
MAX_LENGTH = 300
NUM_RETURN_SEQUENCES = 1

generator = pipeline("text-generation", model=MODEL_PATH)

@app.get("/")
def read_root():
    return {"Hello": "Universe"}

@app.post("/generate/")
def generate_text(item: Item):
    set_seed(42)
    return generator(item.text, max_length=MAX_LENGTH, num_return_sequences=NUM_RETURN_SEQUENCES)