from django.urls import path

from . import views

urlpatterns = [
    path('pre_assessment', views.pre_assessment, name='pre_assessment'),
    path('post_assessment', views.post_assessment, name='post_assessment'),
]