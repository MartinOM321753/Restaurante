from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import SaleDetailViewSet

router = SimpleRouter()

router.register(r'api', SaleDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]