from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'api', UserViewSet, basename='user')

urlpatterns = [
    path('api/user/save/',CreateUserUserView.as_view(), name='create_user'),
    path('api/admin/save/',CreateAdminUserView.as_view(), name='create_admin'),
    path('api/restaurant_owner/save/',CreateRestaurantOwnerUserView.as_view(), name='create_restaurant_owner'),
    path('api/password-reset/request/', RequestPasswordReset.as_view()),
    path('api/password-reset/confirm/', PasswordResetConfirm.as_view())
] + router.urls
