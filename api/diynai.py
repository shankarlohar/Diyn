
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
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
