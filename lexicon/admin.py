from django.contrib import admin
from .models import Language,Concept,Word,Definition,Example,Category
# Register your models here.

admin.site.register(Language),
admin.site.register(Word),
admin.site.register(Definition),
admin.site.register(Concept),
admin.site.register(Example)
admin.site.register(Category)