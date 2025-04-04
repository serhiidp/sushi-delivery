from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from sushi.models.auth import APIKey


class Command(BaseCommand):
    help = "Create API key for user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(username=options["username"])
        key = APIKey.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS(f"API Key: {key.key}"))
