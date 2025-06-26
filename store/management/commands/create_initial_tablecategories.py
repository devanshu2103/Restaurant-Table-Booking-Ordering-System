from django.core.management.base import BaseCommand
from store.models import TableCategory

class Command(BaseCommand):
    help = 'Create initial TableCategory data'

    def handle(self, *args, **kwargs):
        categories = [
            {'category': 4, 'available_tables': 10},
            {'category': 6, 'available_tables': 10},
            {'category': 8, 'available_tables': 10},
        ]
        for cat in categories:
            obj, created = TableCategory.objects.get_or_create(category=cat['category'], defaults={'available_tables': cat['available_tables']})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created TableCategory: {obj}"))
            else:
                self.stdout.write(f"TableCategory already exists: {obj}")
