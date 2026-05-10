from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer


class UserProfileAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
