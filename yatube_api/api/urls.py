from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet


router = DefaultRouter()
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
urlpatterns = [
    path('v1/follow/', FollowViewSet.as_view({'post': 'create',
                                              'get': 'list',
                                              'delete': 'destroy'})),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
