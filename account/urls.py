from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # previous login view
    #path('login/', views.user_login,name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.login_success, name='login_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('parameters/', views.parameters_form, name='parameters'),
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
    # path('KindnessCard/', views.KindnessCard, name='KindnessCard'),
    path('users/', views.users, name='users'),
    path('view-rewards/', views.viewRewards, name='rewards'),
    path('createprogram/', views.createprogram, name='createprogram'),
    path('cloneprogram/', views.cloneprogram, name='cloneprogram'),
    path('analytics/', views.analytics, name='analytics'),
    path('programs/', views.createprogram, name='programs'),

    path('myprogram/', views.myprogram, name='myprogram'),
    path('registerusers/', views.registerusers, name='registerusers'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('cms_frame/', views.cms_frame, name='cms_frame'),
    path('redeem-rewards/', views.rewards_redeem, name='redeem_rewards'),
    path('export_data/', views.export_data, name='export_data'),
    path('django_frame/', views.django_frame, name='django_frame'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('archive/', views.archive, name='archive'),
    path('group_email/', views.group_email, name='group_email'),
    path('send_group_email/', views.send_group_email, name='send_group_email'),
    path('send_individual_email/<int:pk>/', views.email_individual, name='send_individual_email'),
    path('inactive_users/',views.user_inactivity,name='user_inactivity'),
    path('rewards_notification',views.rewards_notification, name='rewards_notification'),
    path('manage_points/', views.manage_points, name='manage_points'),
    path('update_points/', views.update_points, name='update_points'),
    path('admin_edit/', views.admin_edit, name='admin_edit'),

]
