"""
Django cmmand to wait fo rthe database to be available

Due to file structure, Django will see this is a management command
    and will be able to run it with manage.py [command]
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        # log to console as running
        self.stdout.write("Waiting for database...")
        db_up = False  # initialize ready state as false
        while db_up is False:
            try:
                # if db not ready it raises exception
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        # writes when db is available, .SUCCESS prints as green
        self.stdout.write(self.style.SUCCESS('Database available!'))
