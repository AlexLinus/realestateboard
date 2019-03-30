from django.urls import path
from .views import BlogView, PostView, BlogArchiveView, BlogSearchView

urlpatterns = [
    path('', BlogView.as_view(), name='blog_url'),
    path('search/', BlogSearchView.as_view(), name='blog_search_url'),
    path('<str:post_slug>/', PostView.as_view(), name='post_url'),
    path('archive/<str:month>/<str:year>/', BlogArchiveView.as_view(), name='blog_archive_url'),
]
