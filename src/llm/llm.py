from openai import embeddings
from src.llm.llm_config import CLIENT, INDEX

class LLM:
    @staticmethod
    async def get_embeddings(text: str):
        response = embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding

    @staticmethod
    async def search_in_pinecone(query: str):
        query = INDEX.query(await LLM.get_embeddings(query), top_k=10, include_metadata=True)
        return query

    @staticmethod
    async def generate_response(prompt: str):
        search_results = await LLM.search_in_pinecone(prompt)

        context = search_results
        sys_prompt = """
TODO: Add a system prompt here
"""

        stream = CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Context: {context}",
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            stream=True,
        )

        response = ""

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content

        return response
    
