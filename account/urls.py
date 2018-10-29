from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # previous login view
    #path('login/', views.user_login,name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('edit/', views.edit, name='edit'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('users/', views.users, name='users'),
    path('createprogram/', views.createprogram, name='createprogram'),
    path('programs/', views.createprogram, name='programs'),

    path('myprogram/', views.myprogram, name='myprogram'),
    path('registerusers/', views.registerusers, name='registerusers'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('cms_frame/', views.cms_frame, name='cms_frame'),
    path('django_frame/', views.django_frame, name='django_frame'),
    path('profile/<int:pk>/', views.profile, name='profile'),

]
