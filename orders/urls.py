from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import OrdersViewSet

router = SimpleRouter()
router.register(r'api', OrdersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
