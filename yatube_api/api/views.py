from rest_framework import (
    viewsets, permissions, serializers, mixins, status, filters
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model

from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadAndPostOnly


User = get_user_model()


class GetPostDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class FollowViewSet(GetPostDeleteViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> 'QuerySet[Follow]':
        """Получает кверисет из всех подписок текущего юзера."""
        current_user = self.request.user
        return current_user.follower.all()

    def perform_create(self,
                       serializer: serializers.ModelSerializer) -> Response:
        """
        Добавляет текущего юзера в качестве подписчика и создаёт объект в БД.
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs) -> Response:
        """Удаляет подписку."""
        user = request.user
        following_username = request.data['following']
        following = get_object_or_404(User, username=following_username)

        instance = get_list_or_404(Follow, user=user, following=following)[0]
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadAndPostOnly,)

    def perform_create(self,
                       serializer: serializers.ModelSerializer) -> Response:
        """Добавляет автора и дату к посту и создаёт объект в БД."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadAndPostOnly,)

    def get_queryset(self) -> 'QuerySet[Comment]':
        """Получает кверисет из всех комментариев к посту."""
        return get_object_or_404(Post,
                                 pk=self.kwargs['post_id']).comments.all()

    def perform_create(self,
                       serializer: serializers.ModelSerializer) -> Response:
        """
        Добавляет автора, дату и пост к комментарию и создаёт объект в БД.
        """
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs['post_id'])
        )
