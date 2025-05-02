from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
                'user' : user_serializer.data
            })
        else:
            return Response({'detail':'Invalid credentials'}, status=401)

class DashboadView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Welcome to dashboard',
            'user': user_serializer.data
        }, 200)