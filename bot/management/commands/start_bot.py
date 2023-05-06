import argparse

from django.core.management import BaseCommand

from ...tg import bots


class Command(BaseCommand):

    def add_arguments(self, parser: argparse.ArgumentParser):
        choices = [b.name for b in bots.BOTS]
        parser.add_argument('-n', '--name', help='Ignore db entries', required=True, choices=choices)

    def handle(self, *args, **options):
        for bot in bots.BOTS:
            if bot.name == options['name']:
                bot.start()
                return
        raise ValueError(f'Bot with name {options["name"]} not found')
