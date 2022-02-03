from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.versioning import URLPathVersioning
from posts.models import Post, Group, Comment, Follow
from .serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
from .permissions import IsAuthorOrReadOnly, ReadOnly


class FirstVersioning(URLPathVersioning):
    """Defines the api urls path version for applying in viewsets."""
    default_version = 'v1'
    allowed_versions = 'v1'


class PostViewSet(viewsets.ModelViewSet):
    versioning_class = FirstVersioning
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return (ReadOnly(), )
    #     return super().get_permissions()


class GroupViewSet(viewsets.ModelViewSet):
    versioning_class = FirstVersioning
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    versioning_class = FirstVersioning
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        comments_queryset = Comment.objects.filter(post=post_id)
        return comments_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    versioning_class = FirstVersioning
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
