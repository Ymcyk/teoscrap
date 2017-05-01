from urllib.parse import urljoin
from lxml import html
import requests

from .elements import SlugsElements, ArticleElements
from .utils import string_to_words_list

class BlogScraper:
    base_url = 'http://build.sh'

    def __init__(self):
        self.slugs_elements = SlugsElements(self.base_url)
        self.article_elements = ArticleElements()

    def scrap(self):
        #from datetime import datetime
        #urls = self.slugs_elements.scrapall(datetime(2016, 2, 15))
        #for url in urls:
        #    print(url)
        #print('urls:', len(urls))
        art = self.article_elements.scrap('http://build.sh/kickstarter-we-are-a-backer/')
        print('TITLE:', art.title)
        print('date:'.upper(), art.date)
        print('AUTHOR:', art.author)
        print('TEXT:', string_to_words_list(art.text))

