from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('news/', views.news, name='news'),
    path('news/<slug:slug>/', views.news_details, name='news_details'),
    path('contact/', views.contact, name='contact'),
    path('clients/', views.clients, name='clients'),
    path('team/', views.team, name='team'),
]
