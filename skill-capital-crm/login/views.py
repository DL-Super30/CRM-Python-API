from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, LoginSerializer

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # permission_classes=[permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
         return Response({"message":"succes"},status=status.HTTP_200_OK)
        else:
         return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        # if user:
        #     token, created = Token.objects.get_or_create(user=user)
        #     return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

