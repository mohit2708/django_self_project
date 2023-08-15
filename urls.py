from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views  # direct logout by auth 


urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', login_required(views.home, login_url='login'), name='home'),
    path('logout/', views.custom_logout, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # direct logout by auth
    path('send_email/', views.send_email, name='send_email'),

]
