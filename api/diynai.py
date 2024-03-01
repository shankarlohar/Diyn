
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain.agents import Tool
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.agents import ZeroShotAgent
import os

load_dotenv()

# Creating a connection URL for PostgreSQL
db_url = f"postgresql://{os.getenv('username')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database_name')}"

# Create SQLAlchemy engine
engine = create_engine(db_url)

# Create SQLDatabase instance
sql_database = SQLDatabase(engine)

llm = GoogleGenerativeAI(model="models/text-bison-001",
                         google_api_key=os.getenv('GOOGLE_API_KEY'), temperature=0.1)

# Now you can use the engine to create a SQLDatabaseChain
sql_chain = SQLDatabaseChain.from_llm(llm, sql_database, verbose=True)

tools = [
    Tool(
        name="Search",
        func=sql_chain.run,
        description="You are a chatbot that can answer questions about specific events",
    )
]

prefix = """Interact with a human by answering the questions by accessing the following tools:"""
suffix = """Begin!"

{history}
Query: {input}
{agent_scratchpad}"""
# configure the structure for the interface of the chat
prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "history", "agent_scratchpad"],
)
memory = ConversationBufferMemory(memory_key="history")

llm_chain = LLMChain(llm=llm, prompt=prompt)

agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)

agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory)

print("\n\nCHATBOT READY!\n\n")
