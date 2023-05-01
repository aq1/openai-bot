from .request import create_chat_completion


async def summarize_text(language: str, text: str) -> str:
    command = {
        'ru': 'Переведи на русский и напиши краткое содержание в 40 словах:',
        'en': 'Summarize text in 40 words:'
    }[language]

    response = await create_chat_completion(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': f'{command}\n\n{text}'},
        ],
    )

    try:
        return response['choices'][0]['message']['content']
    except (IndexError, KeyError):
        return ''
