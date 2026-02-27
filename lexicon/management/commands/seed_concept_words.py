import os
import json
from django.conf import settings
from django.db import transaction # Standard for data integrity
from lexicon.models import Category, Concept, Word, Language
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seeds Concepts and Words safely with transaction integrity'

    def handle(self, *args, **options):
        path_file = os.path.join(settings.BASE_DIR, 'seeds', 'concepts_seed_identity_self.json')
        
        # 1. Foundation
        german_language_obj, _ = Language.objects.get_or_create(
            code='de',
            defaults={'name': 'German', 'direction': 'ltr'}
        )

        # 2. Open file with CORRECT encoding string
        try:
            with open(path_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"FILE NOT FOUND: {path_file}"))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("INVALID JSON FORMAT"))
            return

        # 3. The Engine (Wrapped in a transaction)
        try:
            with transaction.atomic():
                # json_data is a LIST, so we must loop it
                for category_group in json_data:
                    
                    category_obj = Category.objects.get(slug=category_group['category_slug'])
                    self.stdout.write(self.style.SUCCESS(f"PROCESSING CATEGORY: {category_obj.name}"))

                    # Loop through the CONCEPTS in the JSON group (not the model)
                    for concept_data in category_group['concepts']:
                        concept, _ = Concept.objects.get_or_create(
                            semantic_key=concept_data['semantic_key'],
                            defaults={
                                'description': concept_data['description'],
                                'category': category_obj
                            }
                        )

                        words_array = concept_data['related_german_words']
                        for word_str in words_array:
                            # Using update_or_create ensures we safely update existing records
                            Word.objects.update_or_create(
                                text=word_str,
                                language=german_language_obj,
                                defaults={
                                    'concept': concept,
                                    'pos': 'noun',
                                    'metadata': {}
                                }
                            )
                            
            self.stdout.write(self.style.SUCCESS("SEEDING COMPLETE. ALL WORDS SAVED."))

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("A CATEGORY SLUG IN JSON DOES NOT EXIST IN DB. TRANSACTION ROLLED BACK."))
        except Exception as e:
            # Tell the absolute truth about the error
            self.stdout.write(self.style.ERROR(f"CRITICAL FAILURE: {str(e)}. TRANSACTION ROLLED BACK."))