import json
import pathlib

from django.core.management import BaseCommand

from ...models import BotText


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = pathlib.Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'bot_text.json'
        with open(path, encoding='utf8') as f:
            texts = json.load(f)

        for text in texts:
            fields = text['fields']
            bot_text, created = BotText.objects.get_or_create(
                label=fields['label'],
                defaults=dict(
                    ru=fields['ru'],
                    en=fields['en'],
                ),
            )

            print(f'{bot_text.label} -> {created}')
