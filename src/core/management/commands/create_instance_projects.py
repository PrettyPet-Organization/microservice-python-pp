from django.core.management.base import BaseCommand

from core.fixtures import create_instance_projects


class Command(BaseCommand):
    help = "Populate the database with initial data"

    def handle(self, *args, **kwargs):
        create_instance_projects()
        self.stdout.write(self.style.SUCCESS("Database has been populated with initial data."))
