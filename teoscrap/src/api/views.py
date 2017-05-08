from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.http import Http404

from blog.models import ArticleWord, Author

class StatList(APIView):
    '''
    View class for /stats/ and /stats/<author>/ requests
    '''
    allowed_methods = ('GET',)

    def get(self, request, author_slug=None):
        queryset = ArticleWord.objects.all()
        if author_slug:
            try:
                author = Author.objects.get(slug=author_slug)
                queryset = queryset.filter(article__author=author)
            except Author.DoesNotExist:
                raise Http404
        values = queryset.values('word__word').\
                annotate(amount=Sum('words_number')).order_by('-amount')[:10]
        ordered = OrderedDict()
        for val in values:
            ordered[val['word__word']] = val['amount']
        return Response(ordered)
