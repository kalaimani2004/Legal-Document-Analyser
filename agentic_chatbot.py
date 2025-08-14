import os
import time
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from dotenv import load_dotenv
from openai import RateLimitError

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
db_uri = os.getenv("POSTGRES_URI")

# Initialize the language model with the provided OpenAI API key
llm = ChatOpenAI(temperature=0, openai_api_key="")

# Connect to the PostgreSQL database
print("DB URI:", db_uri)
db = SQLDatabase.from_uri(db_uri)

# Initialize the toolkit for the agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create the agent executor for SQL-based interaction
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

def query_openai_with_retry(prompt, retries=2, delay=30):
    """Function to handle rate-limiting and retrying OpenAI API calls."""
    attempt = 0
    while attempt < retries:
        try:
            # Run the agent to get the response
            response = agent_executor.run(prompt)
            return response
        except RateLimitError as e:
            print(f"Rate limit exceeded: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)  # Wait before retrying
            attempt += 1
            if attempt == retries:
                return "Exceeded maximum retry attempts due to rate limit."
    
    return None

def agentic_legal_chatbot(question):
    """Main function to interact with the legal chatbot."""
    response = query_openai_with_retry(question)
    if response is None:
        return "Sorry, I couldn't process your request at this moment."
    return response
