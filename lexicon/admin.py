from django.contrib import admin
from .models import Language,Concept,Word,Definition,Example,Category,Book,Lesson,SentenceTranslation
# Register your models here.

admin.site.register(Language),
admin.site.register(Word),
admin.site.register(Definition),
admin.site.register(Concept),
admin.site.register(Example),
admin.site.register(Category),
admin.site.register(Book),
admin.site.register(Lesson)
admin.site.register(SentenceTranslation)