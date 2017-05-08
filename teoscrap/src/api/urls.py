from django.conf.urls import url

from .views import StatList

urlpatterns = [
    url(r'^$', StatList.as_view()),
    url(r'^(?P<author_slug>\w+)$', StatList.as_view()),
]
