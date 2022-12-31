from django.urls import path
from signals.v1 import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'signals'

urlpatterns = [
    path('get/', views.UserSignalViewSet.as_view()),
    path('coins/', views.CoinsViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
