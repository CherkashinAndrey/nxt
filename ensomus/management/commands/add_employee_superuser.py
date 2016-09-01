from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import getpass
from ensomus.models import Company, Employee


class Command(BaseCommand):
    help = '''Create superuser with comfirmed email address.

    Usage: manage.py add_employee_superuser
    '''

    def add_arguments(self, parser):
        # parser.add_argument('--name', type=str, dest='name', required=True)
        parser.add_argument('--first_name', type=str, dest='first_name', required=True)
        parser.add_argument('--last_name', type=str, dest='last_name', required=True)
        parser.add_argument('--email', type=str, dest='email', required=True)
        parser.add_argument('--is_manager', dest='is_manager', required=True, action='store_true')
        parser.add_argument('--language_code', type=str, dest='language_code', required=True)
        parser.add_argument('--company', type=str, dest='company', required=True)
        parser.add_argument('--phone', type=str, dest='phone', required=True)
        parser.add_argument('--is_superuser', dest='is_superuser', required=False, action='store_true', default=False)
        # parser.add_argument('--manager', type=str, dest='phone', required=True)

    def handle(self, *args, **options):
        passwd = getpass.getpass("Enter password:").strip()
        company = Company.objects.create(name=options['company'])

        user_model = get_user_model()

        users = user_model.objects.filter(email=options['email']).all()

        if users:
            raise CommandError("User with such email/username already exists.")

        if not options['is_superuser']:
            u = user_model.objects.create_user(
                options['email'], options['email'], passwd, first_name=options['first_name'], last_name=options['last_name']
            )
        else:
            u = user_model.objects.create_superuser(
                options['email'], options['email'], passwd, first_name=options['first_name'], last_name=options['last_name']
            )

        u.save()

        Employee.objects.create(user=u, is_manager=options['is_manager'], language_code=options['language_code'],
                                company=company, phone=options['phone'])