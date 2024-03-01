from fastapi import FastAPI
from diynai import sql_chain
from model import Query

app = FastAPI()

print("CHATBOT READY!")


@app.get("/")
async def root(token: Query):

    result = sql_chain.invoke(token.question)

    return result
