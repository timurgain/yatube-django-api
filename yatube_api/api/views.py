from rest_framework import viewsets
from rest_framework.versioning import URLPathVersioning
from posts.models import Post, Group, Comment, Follow
from .serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer


class FirstVersioning(URLPathVersioning):
    """Defines the api urls path version for applying in viewsets."""
    default_version = 'v1'
    allowed_versions = 'v1'


class PostViewSet(viewsets.ModelViewSet):
    versioning_class = FirstVersioning
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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


class FollowViewSet(viewsets.ModelViewSet):
    versioning_class = FirstVersioning
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
