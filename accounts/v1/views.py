from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, RegisterSerializer, CheckTransferSerializer
from accounts.v1.serializers import UserSerializer, PlanSerializer, ProfileSerializerF, UserSerializerF, WalletSerializer
from accounts.models import Plan, Profile, WalletAddress
from django.shortcuts import get_object_or_404
from rest_framework import status

from accounts.v1.functions import check_token, check_transfer

User = get_user_model()

# Class based view to Get User Details using Token Authentication


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Class based view to register user


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        email = response.data['email']
        user = User.objects.get(email=email)
        token = Token.objects.get(user=user)
        return Response(
            {
                'Success': True,
                'UserId': user.pk,
                'Email': response.data['email'],
                'Token': token.key,
            })


class LoginUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                email = request.data['email']
                user = User.objects.get(email=email)
            except:
                raise ValidationError(
                    {
                        'Success': False,
                        'ErrorCode': 105,
                        'ErrorMessage': 'کاربر با این آدرس ایمیل وجود ندارد',
                    }
                )

            if not check_password(request.data['password'], user.password):
                raise ValidationError(
                    {
                        'Success': False,
                        'ErrorCode': 106,
                        'ErrorMessage': 'پسورد اشتباه است',
                    }
                )

            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'Success': True,
                    'UserId': user.pk,
                    'Email': user.email,
                    'Token': token.key,
                })
        else:
            raise ValidationError(serializer.errors)


class PlanViewSet(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserProfileViewSet(APIView):
    def post(self, request):
        token = request.data['token']
        user = check_token(token)
        serializer = UserSerializerF(user)
        return Response(serializer.data)


class CheckTransferViewSet(APIView):

    def post(self, request, format=None):
        serializer = CheckTransferSerializer(data=request.data)
        if serializer.is_valid():
            data = {}
            user = check_token(request.data['token'])
            transfer = check_transfer(
                user=user, hash=request.data['txid'], plan_id=request.data['plan'])

            data['token'] = serializer.data['token']
            data['transfer_status'] = transfer

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletViewSet(generics.ListAPIView):
    serializer_class = WalletSerializer
    queryset = WalletAddress.objects.all()

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
