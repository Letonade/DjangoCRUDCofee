from rest_framework import viewsets
from CRUDCofee.models import CofeeMixModel
from CRUDCofee.interfaces.api.serializers.cofee_mix_entry_serializer import CofeeMixSerializer

class CofeeMixViewSet(viewsets.ModelViewSet):
    """
    ViewSet qui gère les opérations CRUD pour les mixes de café.
    """
    queryset = CofeeMixModel.objects.all()
    serializer_class = CofeeMixSerializer
