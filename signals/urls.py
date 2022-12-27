from django.urls import path
from signals import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'signals'

urlpatterns = [
    path('get/', views.SignalViewSet.as_view()),
    path('getByEmail/', views.SignalByEmailViewSet.as_view(), name='signal_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
