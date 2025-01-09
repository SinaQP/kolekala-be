from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProductCategoryViewSet, ShopViewSet

router = DefaultRouter()
router.register(r'category', ProductCategoryViewSet)
router.register(r'shops', ShopViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
