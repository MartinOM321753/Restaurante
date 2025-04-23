from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'api', MenuViewSet)  # Deja 'api' aquí, no lo cambies

urlpatterns = [
    path('', include(router.urls)),
    path('findByRestaurant/<int:restaurant_id>/',findMenusByRestaurant.as_view(),name='find-menus-by-restaurant')
]
