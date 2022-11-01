from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .serializers import (  # isort:skip
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from .permissions import IsAdminOrReadOnly  # isort:skip
from reviews.models import Category, Genre, Title  # isort:skip


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = "name"


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = "name"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")
