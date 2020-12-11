from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet

router = DefaultRouter()

router.register('titles/(?P<titles_id>.+)/reviews', ReviewViewSet,
                basename='reviews-list')
router.register('titles/(?P<titles_id>.+)/reviews/(?P<reviews_id>.+)/comment',
                CommentViewSet, basename='comments-list')

urlpatterns = [
    path('v1/', include(router.urls)),
    ]
