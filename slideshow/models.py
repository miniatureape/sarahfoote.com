from django.db import models

class SlideShowImage(models.Model):
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="slideshow")

    class Meta:
        ordering = ['-modified',]
