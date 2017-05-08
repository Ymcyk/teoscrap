from django.core.management.base import BaseCommand
from datetime import datetime
import logging

from scrapers.blog import BlogScraper
from scrapers.utils import string_to_date
from blog.models import ArticleWord, Article

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        newest = Article.objects.all().order_by('-date')
        date = newest[0].date if newest else None
        blog = BlogScraper()
        blog.scrap(date)
