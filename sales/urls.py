from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'api', SaleViewSet, basename='sales')

urlpatterns = [
    path('', include(router.urls)),
    path('restaurantMostSoldFoods/<int:restaurant_id>/',MostSoldFoodsView.as_view(),name="most-sold-foods-by-restaurant"),
    path('globalMostSoldFoods/',MostSoldFoodsGlobalView.as_view() ,name="most-sold-global-foods"),
    path('restaurantSales/<int:restaurant_id>/', SalesByRestaurantView.as_view(), name='sales-by-restaurant'),

    path('userSales/<int:user_id>/',SalesByUserView.as_view(),name='sale-by-user')

]
