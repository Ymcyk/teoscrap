from django.db import IntegrityError
from urllib.parse import urljoin
from lxml import html
import requests
import logging

from blog.models import ArticleWord, Author, Article
from .elements import SlugsElements, ArticleElements

logger = logging.getLogger(__name__)

class BlogScraper:
    base_url = 'http://build.sh'

    def __init__(self):
        self.slugs_elements = SlugsElements(self.base_url)
        self.article_elements = ArticleElements()

    def scrap(self, date=None):
        urls = self.slugs_elements.scrapall(date)

        logger.warning('Scraping...')
        art_l = self.__scrap_new_articles(urls)
        
        if not len(art_l):
            logger.warning('No new articles to scrap')
            return

        logger.warning('Saving...')
        for itr in range(len(art_l)):
            logger.warning('{}/{}'.format(itr+1, len(art_l)).ljust(6) \
                    + art_l[itr].title)

            author = Author.objects.get_or_create(name=art_l[itr].author)[0]
            
            article = Article.objects.create(
                title=art_l[itr].title,
                author=author,
                date=art_l[itr].date,
            )
            ArticleWord.assign_text_to_article(art_l[itr].text, article)
        logger.warning('Scraping done')

    def __scrap_new_articles(self, urls):
        art_l = []
        for itr in range(len(urls)):
            art = self.article_elements.scrap(urls[itr])
            try:
                Article.objects.get(title=art.title)
            except Article.DoesNotExist:
                art_l.append(art)
        return art_l
