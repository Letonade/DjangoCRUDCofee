from rest_framework import serializers
from CRUDCofee.models import CofeeBeanModel

class CofeeBeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CofeeBeanModel
        fields = ['id', 'name', 'description', 'certificate_valid']
        read_only_fields = ['certificate_valid']

    def create(self, validated_data):
        """
        Assigne toujours certificate_valid=False lors de la création.
        """
        validated_data['certificate_valid'] = False
        return super().create(validated_data)
