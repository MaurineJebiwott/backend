# contracts/views.py
from rest_framework import generics, permissions
from .models import Contract
from .serializers import ContractSerializer

class ContractListCreateView(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Auto-assign logged in user as cedent
        serializer.save(cedant=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == "cedant":  # adjust based on your User model roles
            return Contract.objects.filter(cedant=user)
        elif user.role == "reinsurer":
            return Contract.objects.filter(status="draft") | Contract.objects.filter(reinsurer=user)
        return Contract.objects.none()

class ContractUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        contract = self.get_object()
        if user.role == "reinsurer":
            # Reinsurer can accept/reject
            status = self.request.data.get("status")
            share_percentage = self.request.data.get("share_percentage")
            if status == "active":
                serializer.save(reinsurer=user, status="active", share_percentage=share_percentage)
            elif status in ["expired", "rejected"]:
                serializer.save(reinsurer=user, status=status)
        else:
            serializer.save()  # Cedent can only edit coverage, type, dates while draft
