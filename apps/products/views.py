from apps.core.views import ModelViewSet
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['name', 'description', 'price', 'category']
    search_fields = ['name', 'description']


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']
