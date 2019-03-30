from django.urls import path
from .views import ClassifiedView, ClassifiedEdit, DeleteClassifiedView, ComplaintsView, SearchClassifiedView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('search/', SearchClassifiedView.as_view(), name='classified_search_url'),
    path('<str:flat_slug>/', ClassifiedView.as_view(), name='flat_detail_url'),
    path('<str:flat_slug>/edit/', login_required(ClassifiedEdit.as_view()), name='edit_classified_url'),
    path('<str:flat_slug>/delete/', login_required(DeleteClassifiedView.as_view()), name='delete_classified_url'),
    path('<str:flat_slug>/complaint/', ComplaintsView.as_view(), name='complaint_classified_url'),
]
