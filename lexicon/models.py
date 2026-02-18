from django.db import models

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


class Concept(models.Model):
    """
    The 'Semantic Anchor'
    """
    description= models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Concept ID: {self.id}"
    

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

    concept = models.ForeignKey(Concept,related_name='words',on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    text = models.CharField(max_length=255,db_index=True)
    pos = models.CharField(max_length=20,choices=POS_CHOICES)
    audio_url = models.URLField(blank=True,null=True)

    metadata = models.JSONField(default=dict, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['language','text','pos'],
                name='unique_word_per_language_pos'
            )
        ]



class Example(models.Model):
    text = models.TextField()
    translation = models.TextField(blank=True,null=True)
    translation_language= models.ForeignKey(Language, on_delete=models.CASCADE)
    audio_url = models.URLField(blank=True,null=True)

    
class Definition(models.Model):
    word = models.ForeignKey(Word,related_name='definition',on_delete=models.CASCADE)
    language = models.ForeignKey(Language,on_delete=models.CASCADE)

    text = models.CharField()

    linked_examples = models.ManyToManyField(Example,blank=True)
