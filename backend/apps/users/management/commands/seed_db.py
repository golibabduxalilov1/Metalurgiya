"""
Management command: seed_db
Creates only the default admin user.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create the default admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-password',
            type=str,
            default='Admin1234',
            help='Password for admin user',
        )

    def handle(self, *args, **options):
        self.stdout.write('Creating default admin user...')
        self._create_admin(options['admin_password'])
        self.stdout.write(self.style.SUCCESS('Default admin user is ready.'))

    def _create_admin(self, password):
        if User.objects.filter(username='admin').exists():
            self.stdout.write('  Admin user already exists')
            return

        User.objects.create_superuser(
            username='admin',
            email='admin@machine-registry.local',
            password=password,
            first_name='Admin',
            last_name='System',
            role='admin',
        )
        self.stdout.write(f'  Created admin user (login: admin, password: {password})')
