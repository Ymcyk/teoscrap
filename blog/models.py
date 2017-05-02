from django.core.exceptions import ValidationError
from django.db import models

from .managers import ArticleWordManager
from .utils import slugify, string_to_words_list

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
            self.slug = slugify(self.name)
        super(type(self), self).save(*args, **kwargs)

    def __eq__(self, other):
        return self.slug == other.slug

    def __str__(self):
        return self.name

class Word(models.Model):
    word = models.CharField(
        max_length=255,
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.word = self.word.lower()
        super(type(self), self).save(*args, **kwargs)

    def __eq__(self, other):
        return self.word == other.word

    def __str__(self):
        return self.word

class Article(models.Model):
    title = models.CharField(
        max_length=255,
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )
    date = models.DateField()
    article_words = models.ManyToManyField(
        Word,
        through='ArticleWord',
    )

    def __eq__(self, other):
        return self.title == other.title

    def __str__(self):
        return self.title

class ArticleWord(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
    )
    words_number = models.PositiveIntegerField(
        default=1,
    )

    objects = ArticleWordManager()

    @classmethod
    def assing_words_to_article(cls, article, text):
        words = string_to_words_list(text)
        for word in words:
            w = Word.objects.get_or_create(word=word)[0]
            cls.objects.create(article=article, word=w)

    def __str__(self):
        return '{} - {} {}'.format(self.article, self.word, self.words_number)

