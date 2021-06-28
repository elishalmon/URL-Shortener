from django.db import models
from .generator import create_random_url

class Shortener(models.Model):

    full_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True, blank=True)
    counter = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """
            Save the shortener to DB, after creating the short url and validating the model
        """
        if len(self.short_url) == 0:
            self.short_url = create_random_url(self)
        self.full_clean()
        super(Shortener, self).save(*args, **kwargs)

    def __str__(self):
        return 'From {0} To {1}'.format(self.full_url, self.short_url)




