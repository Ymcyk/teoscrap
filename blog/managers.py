from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class ArticleWordManager(models.Manager):
    def create(self, *args, **kwargs):
        try:
            aw = kwargs['article'].articleword_set.get(word=kwargs['word'])
            aw.words_number += 1
            aw.save()
            return aw
        except ObjectDoesNotExist:
            return super(type(self), self).create(*args, **kwargs)

