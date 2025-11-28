# contracts/urls.py
from django.urls import path
from .views import ContractListCreateView, ContractUpdateView, ParticipateInContractView, AvailableContractsView

urlpatterns = [
    path("contracts/", ContractListCreateView.as_view(), name="contracts-list"),
    path("contracts/<int:pk>/", ContractUpdateView.as_view(), name="contract-update"),
    path("contracts/participate/", ParticipateInContractView.as_view(), name="contracts-participate"),
    path("contracts/available/", AvailableContractsView.as_view(), name="contracts-available"),
]
