from django.core.management.base import BaseCommand, CommandError
class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def handle(self, *args, **options):
        from balance.models import Company
        from balance.mail import send
        from balance.parser import get_table


        all = Company.objects.all().order_by("name")
        get_table(all)
        send()
