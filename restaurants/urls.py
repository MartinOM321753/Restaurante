from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *


router = SimpleRouter()
router.register(r'api',RestaurantViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('findByUser/<int:user_id>/',findByUser.as_view(),name='find-restaurants-by-user'),
    path('findLatest/',getFiveLatest.as_view(),name='latest-restaurants')
]