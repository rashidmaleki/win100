from django.urls import path
from notifications.v1 import views

urlpatterns = [
    path('get/', views.NotificationViewSet.as_view()),
    path('faq/', views.FaqViewSet.as_view()),
]
