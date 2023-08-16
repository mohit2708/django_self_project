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
    path('custom_change_password/', views.custom_change_password, name='custom_change_password'),
    path('forget_password/', views.forgot_password, name='forgot_password'),
    # path('reset-password/<int:user_id>/<str:token>/', views.reset_password, name='reset_password'),
    path('reset-password/<int:user_id>/<str:reset_token>/', views.reset_password_confirm, name='reset_password_confirm'),

    path('reset_password/', views.reset_password_request, name='reset_password_request'),
    path('reset_password_done/', views.reset_password_done, name='reset_password_done'),
    # path('reset_password_confirm/<str:reset_token>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('password_reset_success/', views.password_reset_success, name='password_reset_success'),
    path('password_reset_failed/', views.password_reset_failed, name='password_reset_failed'),




]
