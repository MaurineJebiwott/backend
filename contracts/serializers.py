# contracts/serializers.py

from rest_framework import serializers
from .models import Contract, ReinsurerParticipation


# -----------------------------------
# PARTICIPATION SERIALIZER
# -----------------------------------
class ParticipationSerializer(serializers.ModelSerializer):
    reinsurer_name = serializers.CharField(source="reinsurer.username", read_only=True)

    class Meta:
        model = ReinsurerParticipation
        fields = [
            "id",
            "contract",
            "reinsurer",
            "reinsurer_name",
            "percentage_taken",
            "status",
            "created_at",
        ]
        read_only_fields = ["reinsurer", "created_at"]


# -----------------------------------
# CONTRACT SERIALIZER
# -----------------------------------
class ContractSerializer(serializers.ModelSerializer):
    cedant_name = serializers.CharField(source="cedant.username", read_only=True)
    participations = ParticipationSerializer(many=True, read_only=True)
    remaining_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            "id",
            "type",
            "cedant",
            "cedant_name",
            "start_date",
            "end_date",
            "coverage",
            "total_percentage",
            "allocated_percentage",
            "remaining_percentage",
            "status",
            "created_at",
            "participations",
        ]
        read_only_fields = ["cedant", "created_at", "allocated_percentage", "status"]

    def get_remaining_percentage(self, obj):
        return obj.remaining_percentage()
