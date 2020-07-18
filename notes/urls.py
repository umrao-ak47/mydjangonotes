from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.index, name='index'),
    path('notes/',views.user_home, name='user_home'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', 
    views.note_detail, name='note_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/update', 
    views.note_update, name='note_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/delete', 
    views.note_delete, name='note_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='notes/login.html'),
    name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='notes/logout.html'),
    name='logout'),
    path('new/', views.note_create, name='note_create'),
]