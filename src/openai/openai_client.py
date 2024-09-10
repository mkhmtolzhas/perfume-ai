from openai import OpenAI
from config import OPENAI_API_KEY

CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
)