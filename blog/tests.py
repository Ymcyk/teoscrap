from django.test import TestCase
from datetime import date

from .utils import string_to_words_list, slugify 
from .models import Author, Word, Article, ArticleWord

class UtilsTestCase(TestCase):
    def test_string_to_words_list(self):
        # prepare
        words = ['C++', 'Java', 'Python', '100', 'he\'s', 'words\'']
        string = '{0}, !?.{1}, {2} {3} {4} {5}.'.format(*words)
        # do
        result = string_to_words_list(string)
        # check
        self.assertEqual(words, result, msg="Result is not the same")

    def test_slugify(self):
        # prepare
        name = 'Zażółć gęślą jaźń'
        aim = 'zazolcgeslajazn'
        # do
        result = slugify(name)
        # check
        self.assertEqual(result, aim)

    def test_slugify_fail(self):
        # prepare
        name = 'Zażółć gęślą jaźń'
        aim = 'zazolcgeslajaznh'
        # do
        result = slugify(name)
        # check
        self.assertNotEqual(result, aim)

class AuthorTestCase(TestCase):
    def setUp(self):
        self.name = 'Jan Kowalski'
        self.slug = 'jankowalski'
        self.author = Author.objects.create(name=self.name)

    def test_author_created(self):
        # prepare
        author = Author.objects.get(name=self.name)
        # check
        self.assertEqual(str(author), self.name)

    def test_author_slug_created(self):
        # check
        self.assertEqual(self.author.slug, self.slug)

class WordTestCase(TestCase):
    def setUp(self):
        self.text = 'Python'
        self.word = Word.objects.create(word=self.text)

    def test_word_is_lower(self):
        # prepare
        l_text = self.text.lower()
        word = Word.objects.get(word=l_text)
        # check
        self.assertEqual(str(word), l_text)

class ArticleTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Jan Kowalski')
        self.title = 'Article title'
        self.date = date(2017, 5, 2)
        self.article = Article.objects.create(title=self.title, 
                author=self.author, date=self.date)

    def test_article_created(self):
        # prepare
        article = Article.objects.get(title=self.title)
        # check
        self.assertEqual(str(article), self.title)

class ArticleWordTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Jan Kowalski')
        self.title = 'Article title'
        self.date = date(2017, 5, 2)
        self.article = Article.objects.create(title=self.title, 
                author=self.author, date=self.date)
        self.word1 = Word.objects.create(word='text1')
        self.word2 = Word.objects.create(word='text2')

    def test_created_with_one_word(self):
        # do
        aw = ArticleWord.objects.create(article=self.article, word=self.word1)
        # check
        self.assertEqual(aw.words_number, 1)

    def test_created_few_times_with_same_word(self):
        # prepare
        w_number = 3
        # do
        for _ in range(w_number):
            ArticleWord.objects.create(article=self.article, word=self.word1)
        aw = ArticleWord.objects.get(article=self.article, word=self.word1)
        # check
        self.assertEqual(aw.words_number, w_number)

    def test_created_few_times_with_diffrent_words(self):
        # prepare
        w1_number = 2
        w2_number = 5
        # do
        for _ in range(w1_number):
            ArticleWord.objects.create(article=self.article, word=self.word1)
        for _ in range(w2_number):
            ArticleWord.objects.create(article=self.article, word=self.word2)
        aw1 = ArticleWord.objects.get(article=self.article, word=self.word1)
        aw2 = ArticleWord.objects.get(article=self.article, word=self.word2)
        # check
        self.assertEqual(aw1.words_number, w1_number)
        self.assertEqual(aw2.words_number, w2_number)

    def test_one_word_diffrent_articles(self):
        # prepare
        article2 = Article.objects.create(title='Title', author=self.author,
                date=self.date)
        a1_number = 2
        a2_number = 3
        # do
        for _ in range(a1_number):
            ArticleWord.objects.create(article=self.article, word=self.word1)
        for _ in range(a2_number):
            ArticleWord.objects.create(article=article2, word=self.word1)
        aw1 = ArticleWord.objects.get(article=self.article, word=self.word1)
        aw2 = ArticleWord.objects.get(article=article2, word=self.word1)
        # check
        self.assertEqual(aw1.words_number, a1_number)
        self.assertEqual(aw2.words_number, a2_number)

    def test_assign_text_to_article(self):
        # prepare
        text = 'Python, Python, Django and Django'
        # do
        ArticleWord.assign_text_to_article(text, self.article)
        word_python = Word.objects.get(word='python')
        word_django = Word.objects.get(word='django')
        aw_python = ArticleWord.objects.get(article=self.article, 
                word=word_python)
        aw_django = ArticleWord.objects.get(article=self.article,
                word=word_django)
        # check
        self.assertEqual(aw_python.words_number, 2)
        self.assertEqual(aw_django.words_number, 2)

