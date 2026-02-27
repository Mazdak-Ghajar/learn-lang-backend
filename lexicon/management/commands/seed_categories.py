from django.core.management.base import BaseCommand
import os
import json
from django.conf import settings
from lexicon.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'seeds', 'categories_seed.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                categories = json.load(f)
                for item in categories:
                    category,created = Category.objects.get_or_create(
                        slug=item['slug'],
                        defaults={
                            'name':item['name'],
                            'description':item['description']
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"CREATED: {category.name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"EXISTS: {category.name}"))
                
                self.stdout.write(self.style.SUCCESS("SEEDING COMPLETED"))
        except:
            self.stdout.write(self.style.ERROR("FILE PATH NOT FOUND"))


