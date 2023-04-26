import openai
from django.conf import settings

openai.api_key = settings.OPENAI_KEY


async def summarize_text(text: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"summarize following text:\n{text}"},
        ]
    )

    try:
        return response['choices'][0]['message']['content']
    except (IndexError, KeyError):
        return ''

