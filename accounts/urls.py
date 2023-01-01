from django.urls import path
from accounts.v1 import views

urlpatterns = [
    path('plans/', views.PlanViewSet.as_view()),
    path('register/', views.RegisterUserAPIView.as_view()),
    path('login/', views.LoginUserAPIView.as_view()),
    path('profile/', views.UserProfileViewSet.as_view()),
    path('check_transfer/', views.CheckTransferViewSet.as_view()),
    path('wallets/', views.WalletViewSet.as_view()),
]
