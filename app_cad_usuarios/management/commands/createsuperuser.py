from django.core.management.commands import createsuperuser
from django.utils.translation import gettext_lazy as _

class Command(createsuperuser.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.remove_argument('username')

    def handle(self, *args, **options):
        options['username'] = options['cpf']
        return super().handle(*args, **options)