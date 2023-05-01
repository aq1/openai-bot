import json
import pathlib
import argparse

from django.core.management import BaseCommand

from ...models import BotText


class Command(BaseCommand):
    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--force', action='store_true', help='Ignore db entries')

    def handle(self, *args, **options):
        path = pathlib.Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'bot_text.json'
        with open(path, encoding='utf8') as f:
            texts = json.load(f)

        method = BotText.objects.get_or_create
        if options.get('force'):
            method = BotText.objects.update_or_create

        for text in texts:
            fields = text['fields']
            bot_text, created = method(
                label=fields['label'],
                defaults=dict(
                    ru=fields['ru'],
                    en=fields['en'],
                ),
            )

            print(f'{bot_text.label} -> {created}')
