from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.api import UserProfileAPI
from photos.api import (
    PhotoListAPI, PhotoDetailAPI, CommentListCreateAPI,
    RatingCreateUpdateAPI, LikeToggleAPI, SavedPhotoListAPI,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<str:username>/', UserProfileAPI.as_view(), name='api-user-detail'),
    path('photos/', PhotoListAPI.as_view(), name='api-photo-list'),
    path('photos/<int:pk>/', PhotoDetailAPI.as_view(), name='api-photo-detail'),
    path('photos/<int:pk>/comments/', CommentListCreateAPI.as_view(), name='api-photo-comments'),
    path('photos/<int:pk>/rate/', RatingCreateUpdateAPI.as_view(), name='api-photo-rate'),
    path('photos/<int:pk>/like/', LikeToggleAPI.as_view(), name='api-photo-like'),
    path('saved/', SavedPhotoListAPI.as_view(), name='api-saved-list'),
]
