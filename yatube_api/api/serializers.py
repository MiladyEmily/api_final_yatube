import base64

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data: dict):
        """Преобразует бинарное представление в картинку и наоборот."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='cats.' + ext)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post
        read_only_fields = ('author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        fields = ("user", "following")
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data) -> dict:
        """Проверка, что пользователь не подписывается сам на себя."""
        if data["following"] == self.context.get('request').user:
            raise serializers.ValidationError('Не разрешена подписка на себя')
        return data
