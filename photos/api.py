from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

from .models import Photo, Comment, Rating, Like, SavedPhoto
from .serializers import (
    PhotoSerializer, CommentSerializer,
    RatingSerializer, LikeSerializer, SavedPhotoSerializer,
)


class PhotoListAPI(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PhotoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'caption', 'location', 'tags', 'people_present', 'author__username']

    def get_queryset(self):
        query = Photo.objects.select_related('author').prefetch_related('comments', 'likes', 'ratings')
        term = self.request.GET.get('search')
        if term:
            query = query.filter(
                Q(title__icontains=term) |
                Q(caption__icontains=term) |
                Q(tags__icontains=term) |
                Q(location__icontains=term) |
                Q(people_present__icontains=term) |
                Q(author__username__icontains=term)
            )
        return query.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        ).order_by('-created_at')


class PhotoDetailAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.select_related('author').prefetch_related('comments', 'likes', 'ratings')


class CommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        photo = get_object_or_404(Photo, pk=self.kwargs.get('pk'))
        return photo.comments.select_related('author').order_by('created_at')

    def perform_create(self, serializer):
        photo = get_object_or_404(Photo, pk=self.kwargs.get('pk'))
        serializer.save(photo=photo, author=self.request.user)


class RatingCreateUpdateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        if photo.author == request.user:
            return Response({'detail': "Creators cannot rate their own photos."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating, created = Rating.objects.update_or_create(
            photo=photo,
            user=request.user,
            defaults={'score': serializer.validated_data['score']},
        )
        return Response(RatingSerializer(rating).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class LikeToggleAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        like, created = Like.objects.get_or_create(photo=photo, user=request.user)
        if not created:
            like.delete()
            return Response({'detail': 'Unliked.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Liked.'}, status=status.HTTP_201_CREATED)


class SavedPhotoListAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SavedPhotoSerializer

    def get_queryset(self):
        return SavedPhoto.objects.filter(user=self.request.user).select_related('photo__author').order_by('-created_at')
