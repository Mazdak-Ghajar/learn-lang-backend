from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150,unique=True)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
    
    
class Concept(models.Model):
    """
    The 'Semantic Anchor'
    """
    semantic_key = models.CharField(max_length=255,unique=True)
    description= models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True, blank=True)


    def __str__(self):
        return f"CONCEPT SEMANTIC_KEY: {self.semantic_key}"
    

class Language(models.Model):
    """
    Stores language metadata. 
    Crucial for handling LTR (German) vs RTL (Farsi) in  frontend.
    """

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10,unique=True)
    direction = models.CharField(
        max_length=3,
        choices=[('ltr','Left-to-Right'),('rtl','Right-to-Left')],
        default='ltr'
    )
    def __str__(self):
        return f"{self.name} ({self.code})"




class Book(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=5 , blank=True, null=True)

    def __str__(self):
        return f"{self.title}'Book"
    
class Lesson(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    lesson = models.IntegerField(blank=True, null=True)
    concepts = models.ManyToManyField(Concept,related_name='lesson',blank=True)

    def __str__(self):
        return f"lesson: {self.lesson}"
    

class Word(models.Model):
    """
    The linguistic label for a concept in a specific language. 
    """
    POS_CHOICES = [
        ('noun','Noun'),
        ('verb','Verb'),
        ('adj','Adjective'),
        ('adv','Adverb'),
        ('phrase','Phrase'),
        ('prep','Preposition')
    ]
    LEVEL_CHOICES = [
        ('A1', 'Beginner'),
        ('A2', 'Elementary'),
        ('B1', 'Intermediate'),
        ('B2', 'Upper Intermediate'),
        ('C1', 'Advanced'),
        ('C2', 'Mastery'),
        ('None', 'Uncategorized/Slang') 
    ]

    concept = models.ForeignKey(Concept,related_name='words',on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    text = models.CharField(max_length=255,db_index=True)
    pos = models.CharField(max_length=20,choices=POS_CHOICES)
    audio_url = models.URLField(blank=True,null=True)
    cefr_level = models.CharField(max_length=4, choices=LEVEL_CHOICES, blank=True, null=True)



    metadata = models.JSONField(default=dict, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['language','text','pos'],
                name='unique_word_per_language_pos'
            )
        ]



class Example(models.Model):
    """
    The native sentence in the target language (e.g., German).
    """
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='native_examples')
    text = models.TextField()
    audio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.language.code}: {self.text[:50]}"


class Translation(models.Model):
    """
    The translation of an Example into the user's native language.
    """
    example = models.ForeignKey(Example, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='translated_sentences')
    text = models.TextField()

    class Meta:
        # Crucial Standard: You cannot have two Farsi translations for the exact same German sentence.
        unique_together = ('example', 'language')

    def __str__(self):
        return f"Translation ({self.language.code}) for Example {self.example_id}"

    
class Definition(models.Model):
    word = models.ForeignKey(Word,related_name='definition',on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    text = models.TextField()
    linked_examples = models.ManyToManyField(Example,blank=True)


