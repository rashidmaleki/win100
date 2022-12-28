from django.urls import path
from support.v1 import views

urlpatterns = [
    path('departmans/', views.DepartmansViewSet.as_view()),
    path('ticket/save/', views.TicketSaveViewSet.as_view()),
    path('ticket/get/', views.UserTicketsViewSet.as_view()),
]
