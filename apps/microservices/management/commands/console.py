from django.core.management.base import BaseCommand
from apps.core.views import IocContainer


class Command(BaseCommand):
    help = 'microservice for console'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='*')

    def handle(self, *args, **options):
        container = IocContainer()
        container.console_main()
