from django.shortcuts import render
from django.views.generic import View
from .models import Pages
# Create your views here.
class PageView(View):
    def get(self, request, page_slug):
        page = Pages.objects.get(slug__iexact=page_slug)
        return render(request, 'page_detail.html', context={'page': page })
