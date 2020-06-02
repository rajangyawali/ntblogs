from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('advertisement/', views.advertisement, name='advertisement'),
    path('join/', views.join, name='join'),
    path('privacy/', views.privacy, name='privacy'),
    path('<str:category>/', views.posts, name='posts'),
    path('posts/<slug:slug>/', views.details, name='details'), 
    path('hitcount/', include('hitcount.urls', 'hitcount')),
]