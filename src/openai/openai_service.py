from src.openai.openai_client import CLIENT

class OpenAIService:
    @staticmethod
    async def get_response(prompt: str):
        stream = CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are Abzal, second year student at KBTU. You are a software engineer. You are a laconic person."
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

