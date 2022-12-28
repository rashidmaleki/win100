from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, RegisterSerializer
from accounts.v1.serializers import UserSerializer, PlanSerializer
from accounts.models import Plan, Profile

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
        data = {}
        response = super().create(request, *args, **kwargs)
        email = response.data['email']
        user = User.objects.get(email=email)
        token = Token.objects.get(user=user)
        data["Success"] = True
        data["Email"] = response.data['email']
        data['Token'] = token.key
        return Response(data)


class LoginUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                email = request.data['email']
                user = User.objects.get(email=email)
            except BaseException as e:
                raise ValidationError(
                    {"message": "کاربر با این آدرس ایمیل وجود ندارد"})

            if not check_password(request.data['password'], user.password):
                raise ValidationError(
                    {"message": "پسورد اشتباه است"})

            token = Token.objects.get(user=user)
            return Response({
                'user_id': user.pk,
                'email': user.email,
                'token': token.key,
            })
        else:
            raise ValidationError(serializer.errors)


class PlanViewSet(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer