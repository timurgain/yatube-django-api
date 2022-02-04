from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.versioning import URLPathVersioning

from posts.models import Comment, Follow, Group, Post

from .permissions import IsAuthorOrReadOnly, IsUserOrForbidden
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class FirstVersioning(URLPathVersioning):
    """Defines the api urls path version for applying in viewsets."""
    default_version = 'v1'
    allowed_versions = 'v1'


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for model Post."""
    versioning_class = FirstVersioning
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for model Group."""
    versioning_class = FirstVersioning
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for model Comment."""
    versioning_class = FirstVersioning
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        comments_queryset = Comment.objects.filter(post=post_id)
        return comments_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet for model Follow."""
    versioning_class = FirstVersioning
    serializer_class = FollowSerializer
    permission_classes = (IsUserOrForbidden,)
    filter_backends = (
        filters.SearchFilter,
    )

    # Поиск по '(ForeignKey текущей модели)__(имя поля в связанной модели)'
    search_fields = ('following_id__username',)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
