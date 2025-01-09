from apps.core.views import ModelViewSet
from .models import Product, ProductCategory, Shop
from .serializers import ProductSerializer, ProductCategorySerializer, ShopSerializer


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['name', 'description', 'price', 'category']
    search_fields = ['name', 'description']


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.filter(parent_category=None)
    serializer_class = ProductCategorySerializer
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']
