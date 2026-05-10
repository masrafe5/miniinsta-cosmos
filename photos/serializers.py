from rest_framework import serializers
from .models import Photo, Comment, Rating, Like, SavedPhoto
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'score', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class PhotoSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = [
            'id', 'title', 'caption', 'location', 'people_present', 'tags',
            'image', 'created_at', 'updated_at', 'author',
            'likes_count', 'comments_count', 'average_rating', 'is_saved',
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_entries.filter(user=request.user).exists()
        return False


class SavedPhotoSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(read_only=True)

    class Meta:
        model = SavedPhoto
        fields = ['id', 'photo', 'created_at']
        read_only_fields = ['id', 'photo', 'created_at']
