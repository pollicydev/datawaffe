from django.core.management.base import BaseCommand

from rrap.core.search_logic import index_organisations


class Command(BaseCommand):
    help = "Index all organisations in DW database."

    def handle(self, *args, **options):
        index_organisations()
