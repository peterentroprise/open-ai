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

generate_text_default_prompt = "Once upon a time"

generate_points_default_prompt = "What are the key points from this text:\n\n\"\"\"\nPluto (minor planet designation: 134340 Pluto) is a dwarf planet in the Kuiper belt, a ring of bodies beyond the orbit of Neptune. It was the first and the largest Kuiper belt object to be discovered.\n\nPluto was discovered by Clyde Tombaugh in 1930 and declared to be the ninth planet from the Sun. After 1992, its status as a planet was questioned following the discovery of several objects of similar size in the Kuiper belt. In 2005, Eris, a dwarf planet in the scattered disc which is 27% more massive than Pluto, was discovered. This led the International Astronomical Union (IAU) to define the term \"planet\" formally in 2006, during their 26th General Assembly. That definition excluded Pluto and reclassified it as a dwarf planet.\n\nPluto is the ninth-largest and tenth-most-massive known object directly orbiting the Sun. It is the largest known trans-Neptunian object by volume but is less massive than Eris. Like other Kuiper belt objects, Pluto is primarily made of ice and rock and is relatively small—one-sixth the mass of the Moon and one-third its volume. It has a moderately eccentric and inclined orbit during which it ranges from 30 to 49 astronomical units or AU (4.4–7.4 billion km) from the Sun. This means that Pluto periodically comes closer to the Sun than Neptune, but a stable orbital resonance with Neptune prevents them from colliding. Light from the Sun takes 5.5 hours to reach Pluto at its average distance (39.5 AU).\n\nPluto has five known moons: Charon (the largest, with a diameter just over half that of Pluto), Styx, Nix, Kerberos, and Hydra. Pluto and Charon are sometimes considered a binary system because the barycenter of their orbits does not lie within either body.\n\"\"\"\n\nThe eight key points are:\n\n1."

generate_report_default_prompt = "Read this customer response then answer the following questions:\n\n\"\"\"\nOn March 22 I bought a copy of your game World War Mice. While I enjoyed the beginning of the game I thought the later levels weren't that exciting and the game play was either too easy or impossible. I also thought the graphics were really subpar compared to what was in the video game trailer. I think you can do better and fix it with an update.\n\"\"\"\n\nQuestions:\n1. What product was this about?\n2. Did the customer have complaints?\n3. What as their main comment about the product?\n4. If they were unsatisfied, what can we do to fix this problem?\n5. Was the customer polite?\n\nAnswers:\n1."

class GenerateTextRequest(BaseModel):
    prompt: str = Field(default=generate_text_default_prompt, example=generate_text_default_prompt)
    temperature: float = Field(default=1, example=1)
    max_tokens: int = Field(default=10, example=10)
    top_p: float = Field(default=1, example=1)
    n: int = Field(default=1, example=1)

class GeneratePointsRequest(BaseModel):
    prompt: str = Field(default=generate_points_default_prompt, example=generate_points_default_prompt)
    temperature: float = Field(default=0.5, example=0.5)
    max_tokens: int = Field(default=233, example=233)
    top_p: float = Field(default=1, example=1)

class GenerateReportRequest(BaseModel):
    prompt: str = Field(default=generate_report_default_prompt, example=generate_report_default_prompt)
    temperature: float = Field(default=0.2, example=0.2)
    max_tokens: int = Field(default=64, example=64)
    top_p: float = Field(default=1, example=1)


OPEN_AI_API_KEY = os.environ['OPEN_AI_API_KEY']
openai.api_key = OPEN_AI_API_KEY


@app.get("/")
def read_root():
    return {"Hello": "Universe"}


@app.post("/davinci/")
def generate_text(request: GenerateTextRequest):
    return openai.Completion.create(
        engine="davinci",
        prompt=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        n=request.n
        )

@app.post("/curie/points")
def generate_points(request: GeneratePointsRequest):
    return openai.Completion.create(
  engine="curie",
  prompt=request.prompt,
  temperature=request.temperature,
  max_tokens=request.max_tokens,
  top_p=request.top_p,
  stop=["\"\"\""]
)

@app.post("/curie/report")
def generate_report(request: GenerateReportRequest):
    return openai.Completion.create(
        engine="curie",
        prompt=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stop=["\n\n"]
        )
