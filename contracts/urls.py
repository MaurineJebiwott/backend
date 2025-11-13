# contracts/urls.py
from django.urls import path
from .views import ContractListCreateView, ContractUpdateView

urlpatterns = [
    path("contracts/", ContractListCreateView.as_view(), name="contracts-list"),
    path("contracts/<int:pk>/", ContractUpdateView.as_view(), name="contract-update"),
]
