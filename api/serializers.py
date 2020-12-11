from rest_framework import serializers

from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SlugRelatedField(
        slug_field='rating',
        read_only=True
    )
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Titles
