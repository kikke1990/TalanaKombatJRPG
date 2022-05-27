from django.urls import path
from jrpg.views import TalanaKombatJRPGAPIView

urlpatterns = [
    path('API/talana/kombat',TalanaKombatJRPGAPIView.as_view(),name='api_talana_combat'),
]
