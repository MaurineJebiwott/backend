# contracts/serializers.py
from rest_framework import serializers
from .models import Contract

class ContractSerializer(serializers.ModelSerializer):
    cedent_name = serializers.CharField(source="cedant.username", read_only=True)
    reinsurer_name = serializers.CharField(source="reinsurer.username", read_only=True)

    class Meta:
        model = Contract
        fields = "__all__"
        read_only_fields = ["cedant",]
