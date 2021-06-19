
from django.urls import path
from api import views
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('transactions', views.TransactionAPIView.as_view(), name='transactions'),
    path('mine', views.MineAPIView.as_view(), name='mine'),
    path('full-chain', views.FullChainAPIView.as_view(), name='full-chain'),
    path('nodes/register', views.NodeRegisterAPIView.as_view(), name='node-register'),
    path('nodes/resolve', views.NodeResolveAPIView.as_view(), name='node-resolve'),
    path('device-temp', views.DeviceTempAPIView.as_view(), name='device-temp'),
    path('central-server-command', views.CentralServerCommandAPIView.as_view(),
         name='central-server-command'),
    path('rollback-log', views.RollbackLogAPIView.as_view(), name='rollback-log'),
    path('package-version', views.PackageVersionAPIView.as_view(),
         name='package_version'),
    path('transaction-search', views.TransactionSearchAPIView.as_view(),
         name='transaction-search'),
    path('seed', views.SeedBlockchainAPIView.as_view(), name='seed-blockchain'),
    path('empty-chain', views.EmptyChainAPI.as_view(), name='empty-chain')
]
