from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dashboard import views

router = DefaultRouter()
router.register(r'anlytcs', views.UserActivityViewSet)

urlpatterns = [
    path('', include(router.urls))
]