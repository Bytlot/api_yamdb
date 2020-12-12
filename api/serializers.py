from rest_framework import serializers
from api.models import User, Categories, Genres, Titles, Comment, Review
from rest_framework.validators import UniqueValidator


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')

    def create(self, validated_data):
        if validated_data['role'] == User.Roles.ADMIN:
            return User.objects.create(
                is_staff=True, is_superuser=True, **validated_data)
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        role = validated_data.get('role', None)
        if role == User.Roles.ADMIN:
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()
            return instance
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role')


class EmailRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('email',)


class TokenObtainSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'confirmation_code')


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                        read_only=True)

    def validate(self, data):
        user = self.context['request'].user
        title = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(author=user, title_id=title).exists():
            raise serializers.ValidationError('Оценка поставлена')
        return data

    class Meta:
        fields = ( 'id', 'author', 'text', 'pub_date', 'score')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment