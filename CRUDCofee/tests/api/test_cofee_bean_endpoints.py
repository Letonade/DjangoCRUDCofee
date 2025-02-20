import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCRUDCofee.settings')
django.setup()

import pytest
from django.urls import reverse
from rest_framework import status
from CRUDCofee.infrastructure.models import CofeeBeanModel

@pytest.mark.django_db
class TestCofeeBeanEndpoints:

    def test_create_cofee_bean(self, client):
        url = reverse('cofeebean-list')
        data = {
            "name": "Arabica",
            "description": "Grain premium"
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == "Arabica"
        assert response.data['certificate_valid'] is False

    def test_update_cofee_bean(self, client):
        """
        Vérifie que certificate_valid ne peut pas être modifié avec PUT.
        """
        create_url = reverse('cofeebean-list')
        data = {
            "name": "Moka",
            "description": "Grain de Moka"
        }
        create_response = client.post(create_url, data, content_type='application/json')
        bean_id = create_response.data['id']

        update_url = reverse('cofeebean-detail', kwargs={'pk': bean_id})
        update_data = {
            "name": "Moka Updated",
            "description": "Grain de Moka modifié",
            "certificate_valid": True #must ignore
        }
        response = client.put(update_url, update_data, content_type='application/json')
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]
        assert response.data['name'] == "Moka Updated"
        assert response.data['certificate_valid'] is False

    def test_toggle_certificate(self, client):
        """
        Vérifie que l'endpoint toggle_certificate change bien le statut certificate_valid.
        """
        create_url = reverse('cofeebean-list')
        data = {
            "name": "Java",
            "description": "Grain de Java"
        }
        create_response = client.post(create_url, data, content_type='application/json')
        bean_id = create_response.data['id']
        toggle_url = reverse('cofeebean-toggle-certificate', kwargs={'pk': bean_id})

        response = client.post(toggle_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["certificate_valid"] is True

        response = client.post(toggle_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["certificate_valid"] is False
