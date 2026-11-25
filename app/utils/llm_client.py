import os

import dotenv

dotenv.load_dotenv()

from pydantic import SecretStr

from langchain_openai import ChatOpenAI
MODEL=os.getenv("OPENAI_MODEL")

client = ChatOpenAI(
    model=MODEL,
    base_url=os.getenv("OPENAI_ENDPOINT"),
    api_key=SecretStr(os.getenv("OPENAI_API_KEY"))
)
