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


