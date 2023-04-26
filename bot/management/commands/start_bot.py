from django.core.management import BaseCommand

from ...tg import start_bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_bot()
