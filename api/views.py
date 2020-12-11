from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import Categories, Genres, Titles
from .permissions import IsAuthorOrReadOnly


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    A viewset that provides `list`, `create' and 'delete' and actions.

    """
    pass


class CategoriesViewSet(ListCreateDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer
    permission_classes = [IsAuthorOrReadOnly]


class GenresViewSet(ListCreateDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = serializers.GenresSerializer
    permission_classes = [IsAuthorOrReadOnly]


class TitlesViewSet(ListCreateDeleteViewSet):
    queryset = Titles.objects.all()
    serializer_class = serializers.TitlesSerializer
    permission_classes = [IsAuthorOrReadOnly]
