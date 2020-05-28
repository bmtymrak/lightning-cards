from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify 


class Deck(models.Model):
    name = models.CharField(max_length = 250, blank=False)
    slug = models.SlugField()

    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
         constraints = [
            models.UniqueConstraint(
                fields=['slug', 'user'], 
                name='unique_slug_user'
            )
         ]

class Card(models.Model):
    front = models.CharField(max_length=500, unique=True)
    back = models.TextField()
    deck = models.ManyToManyField(
        Deck,
    )

    def __str__(self):
        return self.front