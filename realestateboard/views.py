from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from classified.models import Classified
from django.contrib.auth import authenticate, login, logout
from classified.forms import UserForm, LoginForm
from blog.models import Post
from classified.forms import SearchClassifiedForm
import datetime
from django.db.models import Count

from urllib.request import urlopen
from bs4 import BeautifulSoup
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

class Home(View):
    def get(self, request):
        classifieds = Classified.objects.filter(is_active=True)[:9]
        search_form = SearchClassifiedForm()
        posts = Post.objects.filter(is_active=True)[:3]
        return render(request, 'index.html', context={'classifieds': classifieds, 'posts': posts, 'search_form': search_form})

class UserClassifieds(View):
    def get(self, request):
        classifieds = Classified.objects.filter(author=request.user)
        return render(request, 'user_classifieds.html', context={'classifieds': classifieds})

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    #отображает пустую форму
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_url')
        else:
            form = self.form_class(None)
            return render(request, self.template_name, context={'form': form})

    # обрабатывает форму
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            user.username = username
            user.email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('home_url')

        return render(request, self.template_name, context={'form': form})

class LoginFormView(View):
    form_class = LoginForm
    template_name = 'login_form.html'
    form = form_class(None)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_url')
        else:
            return render(request, self.template_name, context={'form': self.form, 'wrong_data': False})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home_url')
        else:
            return render(request, self.template_name, context={'form': self.form, 'wrong_data': True})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home_url')


#Для будущего Cron или Celery, для запуска по расписанию
def disactivate_classifieds(request):
    today_date = datetime.date.today()
    month_period = datetime.timedelta(days=20)
    max_date = today_date - month_period
    random_start_date = datetime.date(2019, 1, 1)
    d_classifieds = Classified.objects.filter(pub_date__range=(random_start_date, max_date))
    d_classifieds.update(is_active=False)
    return redirect('home_url')

#Доделать потом парсер. Сложно найти донора для этого, т.к блочат запросы.
def parser(request):
    html = urlopen('https://kaliningrad.cian.ru/kupit-1-komnatnuyu-kvartiru/')
    bsObj = BeautifulSoup(html)
    links = bsObj.select('.c6e8ba5398--header--1Cu_4')
    print(links)
    for item in links:
        link = item.get('href')
        res_ad = urlopen(link)
        soup_ad = BeautifulSoup(res_ad)
        ad_elem = soup_ad.select('.a10a3f92e9--phone--3XYRR')
        print(ad_elem)
        for new_item in ad_elem:
            print(new_item)
    return redirect('home_url')



class AdminPanelView(View):
    def get(self, request):
        today = datetime.date.today()
        total_active_classifieds = Classified.objects.filter(is_active=True).count()
        total_disactive_classifieds = Classified.objects.filter(is_active=False).count()
        today_active_classifieds = Classified.objects.filter(is_active=True, pub_date__day=today.day).count()
        return render(request, 'admin_panel.html', context={'total_active_classifieds': total_active_classifieds, 'today_active_classifieds': today_active_classifieds, 'total_disactive_classifieds': total_disactive_classifieds })

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        'customers': 10,
    }
    return JsonResponse(data)


#Далее мы используем REST API FRAMEWORK. Эти два метода (вьюхи) делают одно и то же.
#Но отличительной особенностью REST API является возможность отдавать данные после аутентификации.
#см. снизу authentication_classes, permission_classes и другие плюшки.
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = []
        values = []

        queryset = Classified.objects.filter(is_active=True).values("pub_date__date").order_by().annotate(Count('id'))
        for item in queryset:
            labels.append(item['pub_date__date'])
            values.append(item['id__count'])
        data = {
            "sales": 100,
            'default_values': values,
            'labels': labels,
        }
        return JsonResponse(data)