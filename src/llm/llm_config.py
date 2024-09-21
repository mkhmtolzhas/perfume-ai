from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
from config import PINECONE_API_KEY, OPENAI_API_KEY

PC = Pinecone(api_key=PINECONE_API_KEY)
INDEX = PC.Index("perfume")
CLIENT = OpenAI(
    api_key=OPENAI_API_KEY
)