"""realestateboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, UserFormView, LoginFormView, LogoutView, UserClassifieds, disactivate_classifieds, parser, AdminPanelView, get_data, ChartData
from classified.views import AddClassidiedView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home_url'),
    path('blog/', include('blog.urls')),
    path('page/', include('pages.urls')),
    path('classified/', include('classified.urls')),
    path('add_classified/', login_required(AddClassidiedView.as_view()), name='add_classified_url'),
    path('my_classifieds/', login_required(UserClassifieds.as_view()), name='user_classifieds_url'),
    path('summernote/', include('django_summernote.urls')),
    path('accounts/register/', UserFormView.as_view(), name='register_url'),
    path('accounts/login/', LoginFormView.as_view(), name='login_url'),
    path('accounts/logout/', login_required(LogoutView.as_view()), name='logout_url'),
    path(r'accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path(r'accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(r'accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(r'accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('disactivate_classifieds/', disactivate_classifieds, name='disactivate_classifieds_url'),
    path('parser/', parser, name='parser'),
    path('admin_panel/', AdminPanelView.as_view(), name='admin_panel_url'),
    path('admin_panel/charts/', get_data, name='admin_panel_charts_url'),
    path('admin_panel/charts/api/', ChartData.as_view(), name='admin_charts_api_url'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

