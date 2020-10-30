from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import pipeline

app = FastAPI(title="Summarization")

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

example_text = "Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24–10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levis Stadium in the San Francisco Bay Area at Santa Clara, California. As this was the 50th Super Bowl, the league emphasized the golden anniversary with various gold-themed initiatives, as well as temporarily suspending the tradition of naming each Super Bowl game with Roman numerals (under which the game would have been known as Super Bowl L), so that the logo could prominently feature the Arabic numerals 50.h and I live in London"


class SumItem(BaseModel):
    text: str = Field(default=example_text, example=example_text)
    min_length: int = Field(default='10', example='10')
    max_length: int = Field(default='100', example='100')




@app.get("/")
def read_root():
    return {"Hello": "Universe"}


@app.post("/summarize/")
def summarize_text(item: SumItem):
    SUM_MODEL_PATH = "/ml-models/facebookbart-large-cnn"

    summarizer = pipeline("summarization", model=SUM_MODEL_PATH,
                      tokenizer=SUM_MODEL_PATH)

    return summarizer(item.text, min_length=item.min_length, max_length=item.max_length)
