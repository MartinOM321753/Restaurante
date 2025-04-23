from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'api', FoodsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('findByMenu/<int:menu_id>/',FindFoodsByMenu.as_view(),name='find-foods-by-menu')

]