from django.core.management.base import BaseCommand
from lexicon.models import Word

class Command(BaseCommand):
    help = 'Finds all German words that the Kaikki miner failed to update'

    def handle(self, *args, **options):
        # Query Postgres directly for words missing the 'morphology' key in their JSONField
        # Note: Depending on your Django version, if metadata is exactly {}, 
        # we can also filter by metadata={}
        missing_words = Word.objects.filter(
            language__code='de'
        ).exclude(
            metadata__has_key='morphology'
        )

        count = missing_words.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("100% of words were successfully updated. No manual work required."))
            return

        self.stdout.write(self.style.WARNING(f"CRITICAL: Found {count} words missing morphology data.\n"))

        # Print them out clearly for manual review
        for word in missing_words:
            self.stdout.write(f"Word: {word.text:<20} | Concept: {word.concept.semantic_key}")
            
        self.stdout.write(self.style.NOTICE(f"\nTotal missing: {count}"))