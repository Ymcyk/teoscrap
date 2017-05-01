from django.db import models

class Author(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models(
        max_length=50,
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        print('ARGS:', args)
        print('KWARGS:', kwargs)
        super(type(self), self).save(*args, **kwargs)

    def __eq__(self, other):
        return self.slug == other.slug

    def __str__(self):
        return self.name

