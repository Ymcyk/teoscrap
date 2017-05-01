from django.core.exceptions import ValidationError
from django.db import models
from trans import trans
import string

class Author(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
    )

    def clean(self):
        if not self.name:
            raise ValidationError('Name field is required')

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = trans(self.name).replace(string.whitespace, '').lower()
        super(type(self), self).save(*args, **kwargs)

    def __eq__(self, other):
        return self.slug == other.slug

    def __str__(self):
        return self.name

