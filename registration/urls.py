from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [   
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('update/', views.edit_profile, name = 'edit_profile'),
    path('changepw/', views.change_password, name = 'change_password'),
    path('posts/create/', views.create, name='create'),
    path('posts/edit/<slug:slug>', views.edit, name='edit'),
    path('posts/delete/<slug:slug>', views.delete, name='delete'),
    path('posts/', views.posts, name='posts'),
    path('images/<slug:slug>', views.add_images, name = 'add_images'), 
]