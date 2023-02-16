from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    """
    Loan serializer
    """
    class Meta:
        model = Loan
        fields = '__all__'
