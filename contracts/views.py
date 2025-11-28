# contracts/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from decimal import Decimal


from .models import Contract, ReinsurerParticipation
from .serializers import ContractSerializer, ParticipationSerializer


# -----------------------------------
# LIST + CREATE CONTRACTS
# -----------------------------------
class ContractListCreateView(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "cedant":
            return Contract.objects.filter(cedant=user)

        if user.role == "reinsurer":
            return Contract.objects.filter(
                Q(status="draft") | Q(participations__reinsurer=user)
            ).distinct()

        return Contract.objects.none()

    def perform_create(self, serializer):
        serializer.save(cedant=self.request.user)


# -----------------------------------
# UPDATE CONTRACT (Cedant only)
# -----------------------------------
class ContractUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        contract = self.get_object()

        if user.role != "cedant":
            return Response(
                {"error": "Only cedants can edit contracts"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)


# -----------------------------------
# REINSURER PARTICIPATION
# -----------------------------------
class ParticipateInContractView(generics.CreateAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        contract_id = request.data.get("contract")
        status_choice = request.data.get("status")

        # Validate contract
        try:
            contract = Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            return Response({"error": "Invalid contract ID"}, status=400)

        # Only reinsurers can participate
        if user.role != "reinsurer":
            return Response({"error": "Only reinsurers can participate"}, status=403)

        # Prevent multiple participations
        if ReinsurerParticipation.objects.filter(contract=contract, reinsurer=user).exists():
            return Response({"error": "You already participated in this contract"}, status=400)

        # ---------------------------------------------
        # HANDLE REJECTION (NO PERCENTAGE REQUIRED)
        # ---------------------------------------------
        if status_choice == "rejected":
            participation = ReinsurerParticipation.objects.create(
                contract=contract,
                reinsurer=user,
                percentage_taken=Decimal("0.00"),
                status="rejected"
            )
            return Response(ParticipationSerializer(participation).data, status=201)

        # ---------------------------------------------
        # HANDLE ACCEPTANCE (PERCENTAGE REQUIRED)
        # ---------------------------------------------
        percentage_raw = request.data.get("percentage_taken")
        try:
            percentage_taken = Decimal(percentage_raw)
        except:
            return Response({"error": "percentage_taken must be a valid number"}, status=400)

        # Check available percentage
        if percentage_taken > contract.remaining_percentage():
            return Response(
                {"error": "Exceeds contract remaining percentage"},
                status=400
            )

        # Create accepted participation
        participation = ReinsurerParticipation.objects.create(
            contract=contract,
            reinsurer=user,
            percentage_taken=percentage_taken,
            status="accepted"
        )

        # Update contract allocated percentage
        contract.allocated_percentage += percentage_taken

        # Update contract status
        if contract.allocated_percentage == contract.total_percentage:
            contract.status = "filled"
        else:
            contract.status = "partially_filled"

        contract.save()

        return Response(ParticipationSerializer(participation).data, status=201)
# -----------------------------------
# AVAILABLE CONTRACTS FOR REINSURERS
# -----------------------------------
class AvailableContractsView(generics.ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "reinsurer":
            #Eclude Contracts wherw=e user already participated
            participated_contract_ids = ReinsurerParticipation.objects.filter(
                reinsurer=user
            ).values_list('contract_id', flat=True)
            
            return Contract.objects.filter(
                allocated_percentage__lt=100
            ).exclude(id__in=participated_contract_ids)
        return Contract.objects.none()
