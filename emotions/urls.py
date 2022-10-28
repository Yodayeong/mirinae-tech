from django.urls import path
from . import views

app_name = 'emotions'

urlpatterns = [
    path('', views.create, name='create'),
    path('index/', views.index, name='index'),
    # path('create/', views.create, name='create'),
]