from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from accounts.serializers import UserSerializer, PlanSerializer
from rest_framework import generics
from accounts.models import Plan
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlanViewSet(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]