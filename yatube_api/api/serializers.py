from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Serializer for model Post."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    pub_date = serializers.DateTimeField(read_only=True)

    # Со slug тут красивее, но тесты не пропускают, хотел бы оставить для себя
    # group = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Group.objects.all(),
    #     required=False,
    #     allow_null=True,
    # )

    class Meta:
        model = Post
        fields = ('id', 'pub_date', 'author', 'text', 'group')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for model Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    created = serializers.DateTimeField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for model Group."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for model Follow."""
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ('user', 'following',)

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='You are already following that author.',
            )
        ]

    def validate(self, attrs):
        request_user = self.context.get('request').user
        following_user = attrs.get('following')
        if request_user == following_user:
            raise serializers.ValidationError("You can't follow yourself.")
        return super().validate(attrs)
