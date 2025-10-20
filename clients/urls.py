from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list_view, name='list'),
    path('<int:pk>/', views.client_detail_view, name='detail'),
]
