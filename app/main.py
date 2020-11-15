from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import openai


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

app = FastAPI(title="Open AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex='https?://.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sample_text = " Tara is my friend"


class InputItem(BaseModel):
    text: str = Field(default=sample_text, example=sample_text)
    max_tokens: int = Field(default=10, example=10)


OPEN_AI_API_KEY = os.environ['OPEN_AI_API_KEY']
openai.api_key = OPEN_AI_API_KEY


@app.get("/")
def read_root():
    return {"Hello": "Universe"}


@app.post("/davinci/")
def generate_text(item: InputItem):
    return openai.Completion.create(
        engine="davinci", prompt=item.text, max_tokens=item.max_tokens)
