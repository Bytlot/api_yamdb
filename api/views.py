from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Reviews, Comment
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination 

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticated]
    pagination_class = PageNumberPagination 

    def get_review(self):
        post = get_object_or_404(Review, id=self.kwargs['rewiew_id'])
        return post

    def get_queryset(self):
        queryset = Comment.objects.filter(title=self.get_review())
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
