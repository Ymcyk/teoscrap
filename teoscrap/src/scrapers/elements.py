from collections import namedtuple
from urllib.parse import urljoin
from lxml import html
import requests

from .utils import string_to_date

class ArticleElements:
    selectors = {
        'title': 'article .post-title',
        'text': 'article .post-content',
        'author': 'article .author-content h4',
        'time': 'time',
    }

    ArticleTuple = namedtuple('ArticleTuple', ['title', 'text', 'author', 'date']) 

    def scrap(self, article_url):
        self.html_content = self.__request_page_content(article_url)
        title = self.__get_title().strip()
        text = self.__get_article_text().strip()
        author = self.__get_author().strip()
        date = self.__get_date()
        return self.ArticleTuple(title=title, text=text, author=author, 
                date=date)

    def __request_page_content(self, url):
        response = requests.get(url)
        return html.fromstring(response.content)

    def __get_title(self):
        return self.__get_element_text(self.selectors['title'])

    def __get_article_text(self):
        return self.__get_element_text(self.selectors['text'])

    def __get_author(self):
        return self.__get_element_text(self.selectors['author'])

    def __get_date(self):
        date_str = self.html_content.cssselect(self.selectors['time'])[0]\
                .attrib['datetime']
        return string_to_date(date_str)

    def __get_element_text(self, element_css):
        element = self.html_content.cssselect(element_css)[0]
        return element.text_content()


class SlugsElements:
    selectors = {
        'slug': '.post-title a',
        'next_page': 'nav .older-posts',
        'article': 'article',
        'time': 'time',
    }

    def __init__(self, base_url):
        self.base_url = base_url

    def scrapall(self, from_date=None):
        urls = []
        next_page = ''

        while True:
            html_content = self.__request_page_content(next_page)
            articles = self.__get_articles(html_content)
            urls += self.__get_articles_urls(articles, from_date)
            next_page = self.__get_next_page_path(html_content)

            if not next_page or len(urls) < len(articles):
                break
        return urls

    def __request_page_content(self, page_num):
        response = requests.get(urljoin(self.base_url, page_num))
        return html.fromstring(response.content)

    def __get_articles(self, html_content):
        return html_content.cssselect(self.selectors['article'])

    def __get_articles_urls(self, articles, from_date=None):
        tags = []
        for article in articles:
            if from_date:
                art_date = string_to_date(article.cssselect(
                    self.selectors['time'])[0].attrib['datetime'])
                if art_date < from_date:
                    continue
            tags.append(article.cssselect(self.selectors['slug'])[0])
        return [urljoin(self.base_url, tag.attrib['href']) for tag in tags]

    def __get_next_page_path(self, html_content):
        tags = html_content.cssselect(self.selectors['next_page'])
        next_page = '' if not tags else tags[0].attrib['href']
        return next_page
