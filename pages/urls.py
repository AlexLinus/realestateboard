from django.urls import path
from .views import PageView

urlpatterns = [
    path('<str:page_slug>/', PageView.as_view(), name='page_url'),
]
