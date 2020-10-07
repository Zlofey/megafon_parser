from django.core.management.base import BaseCommand, CommandError
class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def handle(self, *args, **options):
        from balance import parser
        from balance.models import Company
        parser.get_all(Company.objects.all().order_by("name"))
