# users/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer, UserDocSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Дополнительные действия при создании пользователя, если нужны
        print(f"Пользователь {user.email} успешно зарегистрирован.")


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDocSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
