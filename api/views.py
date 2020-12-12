from django.contrib.auth.tokens import default_token_generator
from django.utils.datetime_safe import datetime
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters, mixins
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser, AllowAny)
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.serializers import RefreshToken
from api.models import User, Review, Comment, Categories, Genres, Titles
from api.serializers import (
    EmailRegistrationSerializer, TokenObtainSerializer,
    UsersSerializer, ProfileSerializer,
    ReviewSerializer, CommentSerializer)
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly

from . import serializers


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UsersSerializer
        return ProfileSerializer

    @action(methods=('GET', 'PATCH'), detail=False,
            permission_classes=(IsAuthenticated,), url_path='me')
    def profile(self, request):
        user = get_object_or_404(
            User, pk=self.request.user.pk)
        serializer = self.get_serializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EmailRegistrationView(GenericAPIView):
    serializer_class = EmailRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.create(
            username=email, email=email, last_login=datetime.now())
        confirmation_code = default_token_generator.make_token(user)
        user.set_password(confirmation_code)
        user.save()
        subject = 'Registration by e-mail'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        message_email = 'confirmation_code %s' % confirmation_code
        send_mail(subject, message_email, from_email, to_email,
                  fail_silently=True)
        return Response(serializer.data)


class TokenObtainView(GenericAPIView):
    serializer_class = TokenObtainSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        confirmation_code = serializer.validated_data['confirmation_code']
        if user.check_password(confirmation_code):
            token = RefreshToken.for_user(user=user)
            user.set_password(None)
            user.save()
            return Response(
                {'refresh': str(token), 'access': str(token.access_token)})
        confirmation_code = default_token_generator.make_token(user)
        user.set_password(confirmation_code)
        user.save()
        subject = 'a new confirmation_code'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        message_email = 'confirmation_code %s' % confirmation_code
        send_mail(subject, message_email, from_email, to_email,
                  fail_silently=True)

        return Response(
            data={'message': ' wrong or already used confirmation_code, '
                             'check your mail for a new confirmation_code'},
            status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAdminOrReadOnly]


class GenresViewSet(ListCreateDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = serializers.GenresSerializer
    permission_classes = [IsAdminOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = serializers.TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]
    pagination_class = PageNumberPagination 

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs['title_id'])
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review,
                                   id=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        queryset = Comment.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)