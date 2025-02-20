from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from CRUDCofee.models import CofeeBeanModel
from CRUDCofee.interfaces.api.serializers.cofee_mix_entry_serializer import CofeeBeanSerializer

class CofeeBeanViewSet(viewsets.ModelViewSet):
    """
    ViewSet qui gère la création, la lecture, la mise à jour et la suppression des grains de café.
    """
    queryset = CofeeBeanModel.objects.all()
    serializer_class = CofeeBeanSerializer

    @action(detail=True, methods=['post'])
    def toggle_certificate(self, request, pk=None):
        """
        Inverse la valeur de certificate_valid pour un bean donné.
        """
        try:
            bean = CofeeBeanModel.objects.get(pk=pk)
            bean.certificate_valid = not bean.certificate_valid  # Inversion True <-> False
            bean.save()
            return Response({'message': 'Certificate validity toggled', 'certificate_valid': bean.certificate_valid},
                            status=status.HTTP_200_OK)
        except CofeeBeanModel.DoesNotExist:
            return Response({'error': 'Bean not found'}, status=status.HTTP_404_NOT_FOUND)
