from fastapi import FastAPI
from diynai import agent_chain as chain
from model import Query

app = FastAPI()


@app.get("/")
async def root(query: Query):

    query.answer = chain.run(query.question)

    return query
