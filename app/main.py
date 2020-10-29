from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import pipeline

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


class SumItem(BaseModel):
    text: str
    min_length: int = Field(default='10', example='10')
    max_length: int = Field(default='100', example='100')


SUM_MODEL_PATH = "facebook-bart-large-cnn"

summarizer = pipeline("summarization", model=SUM_MODEL_PATH,
                      tokenizer=SUM_MODEL_PATH)


@app.get("/")
def read_root():
    return {"Hello": "Universe"}


@app.post("/summarize/")
def summarize_text(item: SumItem):
    return summarizer(item.text, min_length=item.min_length, max_length=item.max_length)
