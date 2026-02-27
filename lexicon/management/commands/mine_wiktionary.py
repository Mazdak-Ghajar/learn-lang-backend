import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from lexicon.models import Word

class Command(BaseCommand):
    help = 'Streams Kaikki JSONL to populate advanced German morphology for Nouns, Verbs, and Adjectives'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, 'seeds', 'wiktionary.jsonl')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"FILE NOT FOUND: {file_path}"))
            return

        self.stdout.write("Pre-loading target vocabulary into RAM...")
        target_words = Word.objects.filter(language__code='de')
        
        vocab_map = {}
        for word in target_words:
            if word.text not in vocab_map:
                vocab_map[word.text] = []
            vocab_map[word.text].append(word)

        if not vocab_map:
            self.stdout.write(self.style.ERROR("No target German words found in DB."))
            return

        words_updated = 0
        self.stdout.write(f"Tracking {len(vocab_map)} unique words. Streaming...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, start=1):
                    
                    data = json.loads(line)
                    word_text = data.get('word')

                    if word_text not in vocab_map:
                        continue
                    
                    pos = data.get('pos')
                    if not pos:
                        continue

                    # Base metadata structure respecting your strict architecture
                    new_metadata = {
                        "morphology": {},
                        "usage_profiles": [] # Left empty for the LLM script later
                    }
                    
                    forms = data.get('forms', [])
                    senses = data.get('senses', [])
                    has_useful_morphology = False

                    # --- NOUN EXTRACTION ---
                    if pos == 'noun':
                        if senses:
                            tags = senses[0].get('tags', [])
                            if 'masculine' in tags: new_metadata['morphology']['gender'] = 'der'
                            elif 'feminine' in tags: new_metadata['morphology']['gender'] = 'die'
                            elif 'neuter' in tags: new_metadata['morphology']['gender'] = 'das'

                        for form in forms:
                            tags = form.get('tags', [])
                            if 'plural' in tags and 'nominative' in tags:
                                new_metadata['morphology']['plural'] = form.get('form')
                                has_useful_morphology = True
                            if 'genitive' in tags and 'singular' in tags:
                                new_metadata['morphology']['genitive'] = form.get('form')
                                has_useful_morphology = True

                    # --- VERB EXTRACTION ---
                    elif pos == 'verb':
                        for form in forms:
                            tags = form.get('tags', [])
                            if 'participle' in tags and 'past' in tags:
                                new_metadata['morphology']['partizip_ii'] = form.get('form')
                                has_useful_morphology = True
                            if 'auxiliary' in tags:
                                new_metadata['morphology']['aux_verb'] = form.get('form')
                                has_useful_morphology = True
                            # Note: Kaikki conjugations are heavily fragmented. 
                            # We grab the Partizip II and Aux as they are the most critical A1-B1 identifiers.

                    # --- ADJECTIVE / ADVERB EXTRACTION ---
                    elif pos in ['adj', 'adjective', 'adv', 'adverb']:
                        # Standardize POS to your database string
                        pos = 'adjective' if 'adj' in pos else 'adverb'
                        
                        for form in forms:
                            tags = form.get('tags', [])
                            if 'comparative' in tags:
                                new_metadata['morphology']['comparative'] = form.get('form')
                                has_useful_morphology = True
                            if 'superlative' in tags:
                                new_metadata['morphology']['superlative'] = form.get('form')
                                has_useful_morphology = True

                    # --- DB UPDATE ---
                    # Only update if we actually found something, otherwise let it remain empty
                    if has_useful_morphology or new_metadata['morphology'].get('gender'):
                        for word_obj in vocab_map[word_text]:
                            word_obj.pos = pos
                            current_meta = word_obj.metadata or {}
                            
                            # Merge morphology but don't overwrite existing usage_profiles
                            if 'morphology' not in current_meta:
                                current_meta['morphology'] = {}
                            current_meta['morphology'].update(new_metadata['morphology'])
                            
                            if 'usage_profiles' not in current_meta:
                                current_meta['usage_profiles'] = []

                            word_obj.metadata = current_meta
                            word_obj.save(update_fields=['pos', 'metadata'])
                            
                        words_updated += 1

                    if line_number % 100000 == 0:
                        self.stdout.write(f"Scanned {line_number} lines...")

            self.stdout.write(self.style.SUCCESS(f"MINING COMPLETE. Updated morphology for {words_updated} words."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"CRITICAL STREAM FAILURE: {str(e)}"))