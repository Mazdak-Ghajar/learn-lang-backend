import os
import json
from django.conf import settings
from lexicon.models import Category,Concept,Word
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        path_file = os.path.join(settings.BASE_DIR, 'seeds' , 'concepts_seed_identity_self.json')

        try:
            with open(path_file, 'r' , encoding='utf=8') as f:
                data = json.load(f)
                category_obj = Category.objects.get(slug=data['category_slug'])
                if category_obj:
                    self.stdout.write(self.style.SUCCESS(f"CATEGORY {category_obj.name} FOUND"))
                    for concept_data in category_obj['concepts']:
                        concept, created = Concept.objects.get_or_create(
                            semantic_key = concept_data['semantic_key'],
                            defaults={
                                'description': concept_data['description'],
                                'category': category_obj
                            }
                        )
        except:
            self.stdout.write(self.style.ERROR("FILE PATH NOT FOUND"))
