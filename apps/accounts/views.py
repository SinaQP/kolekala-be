from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import LoginSerializer, SignUpSerializer
from apps.core.views import APIView


class LoginView(APIView):
    user = None
    serializer_class = LoginSerializer

    def post(self, request):
        request_body = request.data
        self._validate_serializer(request_body)
        email = request_body.get('email')
        password = request_body.get('password')

        self.user = authenticate(request, email=email, password=password)

        if self._is_user_valid():
            return self._send_token()

        return Response({'detail': 'اطلاعات نادرست است.'}, status=status.HTTP_401_UNAUTHORIZED)

    def _is_user_valid(self):
        return self.user is not None

    def _send_token(self):
        token, created = Token.objects.get_or_create(user=self.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class SignupView(APIView):
    user = None
    serializer_class = SignUpSerializer

    def post(self, request):
        request_body = request.data

        self._validate_serializer(request_body)
        email = request_body.get('email')
        password = request_body.get('password')

        if not self._is_email_password_valid(email, password):
            return Response({'detail': 'ایمیل و پسورد باید وارد شوند'}, status=status.HTTP_400_BAD_REQUEST)

        self.user = User.objects.create_user(email=email, password=password)
        self.user = authenticate(request, email=self.user.email, password=self.user.password)

        if self._is_user_valid():
            return self._send_token()

        return Response({'detail': 'اطلاعات نادرست است.'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def _is_email_password_valid(email, password):
        return email is not None or password is not None

    def _is_user_valid(self):
        return self.user is not None

    def _send_token(self):
        token, created = Token.objects.get_or_create(user=self.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)