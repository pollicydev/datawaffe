from django.core.management.base import BaseCommand

from rrap.core.search_logic import clear_index


class Command(BaseCommand):
    help = "Clear organisation index."

    def handle(self, *args, **options):
        clear_index()
