from django.contrib import admin
from .models import Category, Concept, Language, Book, Lesson, Word, Example, Translation, Definition

# --- INLINES (Embedding child models into parent pages) ---

class DefinitionInline(admin.StackedInline):
    model = Definition
    extra = 1 # Shows one blank definition form by default

class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 1

class WordInline(admin.TabularInline):
    model = Word
    extra = 0 # Keeps the Concept page clean until you want to add a word

# --- MAIN ADMIN INTERFACES ---

@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('description',)
    inlines = [WordInline] # Allows adding Words directly from the Concept page!

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'language', 'pos', 'cefr_level', 'concept')
    list_filter = ('language', 'cefr_level', 'pos')
    search_fields = ('text',)
    inlines = [DefinitionInline] # Allows adding Definitions directly on the Word page!

@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('text', 'language')
    list_filter = ('language',)
    search_fields = ('text',)
    inlines = [TranslationInline] # Allows adding Farsi/English translations directly under the German example!

# --- STANDARD REGISTRATIONS ---
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Lesson)