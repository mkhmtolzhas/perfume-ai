from openai import embeddings
from src.llm.llm_config import CLIENT, INDEX
from json import loads

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
        sys_prompt = f"""
Ты — эксперт в мире парфюмерии. Твоя задача — помогать пользователям выбирать ароматы, учитывая их предпочтения, стиль, настроение, а также возможные события, куда они собираются пойти. Всегда предоставляй рекомендации, основываясь на нотах аромата, сезоне, личных предпочтениях и актуальных трендах.
Тебе даются данные из Pinecone, чтобы ты мог использовать их в своих рекомендациях.
Данные из Pinecone:
{context}


Рекомендуй топ 3 аромата для пользователя, учитывая их предпочтения и событие, на которое они собираются.

Помни, что ты — эксперт, и твои рекомендации должны быть обоснованными и аргументированными.
Формат твоего ответа ОБЯЗАТЕЛЬНО должен быть ввиде такого JSON объекта, и должен содержать только JSON объект:
[
    {{
        "name": "Название аромата",
        "brand": "Бренд",
        "type": "Тип аромата",
        "price": "Цена",
        "link": "Ссылка на покупку",
        "image": "Ссылка на изображение (Ссылка обычно выглядит так: https://pcdn.goldapple.ru/p/p/19000017486/web/696d674d61696e8dc83ce5da57a19${{screen}}.${{format}}). Но ты должен его привести в такой вид: https://pcdn.goldapple.ru/p/p/19000017486/web/696d674d61696e8dc83ce5da57a19fullhd.jpg",
        "description": "Описание аромата",
        "notes": "Ноты аромата",
        "opinion": "Почему ты выбрал именно этот аромат",
        "event": "Событие, на которое подходит аромат"
        "season": "Сезон, в котором подходит аромат"
        "style": "Стиль, к которому подходит аромат"
        "pluses": "Плюсы аромата"
        "minuses": "Минусы аромата"
    }},
    {{
        "name": "Название аромата",
        "brand": "Бренд",
        "type": "Тип аромата",
        "price": "Цена",
        "link": "Ссылка на покупку",
        "image": "Ссылка на изображение (Ссылка обычно выглядит так: https://pcdn.goldapple.ru/p/p/19000017486/web/696d674d61696e8dc83ce5da57a19${{screen}}.${{format}}). Но ты должен его привести в такой вид: https://pcdn.goldapple.ru/p/p/19000017486/web/696d674d61696e8dc83ce5da57a19fullhd.jpg",
        "description": "Описание аромата",
        "notes": "Ноты аромата",
        "opinion": "Почему ты выбрал именно этот аромат",
        "event": "Событие, на которое подходит аромат"
        "season": "Сезон, в котором подходит аромат"
        "style": "Стиль, к которому подходит аромат"
        "pluses": "Плюсы аромата"
        "minuses": "Минусы аромата"
    }},
    {{
        "name": "Название аромата",
        "brand": "Бренд",
        "type": "Тип аромата",
        "price": "Цена",
        "link": "Ссылка на покупку",
        "image": "Ссылка на изображение (Ссылка обычно выглядит так: https://pcdn.goldapple.ru/p/p/19000017486/web/696d674d61696e8dc83ce5da57a19${{screen}}.${{format}}). Но ты должен его привести в такой вид: https://pcdn.goldapple.ru/p/p/19000017486/web/696d674d61696e8dc83ce5da57a19fullhd.jpg",
        "description": "Описание аромата",
        "notes": "Ноты аромата, в виде JSON объекта, например: {{ "top": "Верхние ноты", "middle": "Средние ноты", "base": "Базовые ноты" }}",
        "opinion": "Почему ты выбрал именно этот аромат",
        "event": "Событие, на которое подходит аромат"
        "season": "Сезон, в котором подходит аромат"
        "style": "Стиль, к которому подходит аромат"
        "pluses": "Плюсы аромата"
        "minuses": "Минусы аромата"
    }}
]
Будь вежливым и дружелюбным, избегай перегруженности информации, но будь готов дать детализированные рекомендации при необходимости.
"""

        stream = CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"{sys_prompt}",
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

        return loads(response)
