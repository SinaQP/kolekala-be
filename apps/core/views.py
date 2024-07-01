from rest_framework import views, status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class APIView(views.APIView):
    serializer_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['deleted']

    def _validate_serializer(self, request_body):
        serialized_data = self.serializer_class(data=request_body)
        serialized_data.is_valid(raise_exception=True)


class ModelViewSet(viewsets.ModelViewSet):
    serializer_class = None
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    search_fields = []
    ordering = ['created_at']

    # filterset_fields = ['deleted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_default_filterset()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _add_default_filterset(self):
        default_filter_fields = ['deleted', 'created_at', 'updated_at']
        self.filterset_fields += default_filter_fields

    def _validate_serializer(self, request_body):
        serialized_data = self.serializer_class(data=request_body)
        serialized_data.is_valid(raise_exception=True)
