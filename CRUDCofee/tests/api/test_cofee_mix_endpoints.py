import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCRUDCofee.settings')
django.setup()

import pytest
from django.urls import reverse
from rest_framework import status
from CRUDCofee.models import CofeeBeanModel, CofeeMixModel, CofeeMixEntryModel

@pytest.mark.django_db
class TestCofeeMixEndpoints:
    def create_bean(self, name):
        """
        Création directe d'un bean via le modèle pour servir de référence dans les tests.
        """
        return CofeeBeanModel.objects.create(
            name=name,
            certificate_valid=True,
            description=f"Description pour {name}"
        )

    def test_create_mix(self, client):

        bean1 = self.create_bean("Arabica")
        bean2 = self.create_bean("Moka")

        url = reverse('cofeemix-list')
        data = {
            "name": "Mix Test",
            "description": "Un mix de test avec Arabica et Moka",
            "beans": [
                {"bean_id": bean1.id, "quantity": 20},
                {"bean_id": bean2.id, "quantity": 10}
            ]
        }
        response = client.post(url, data, content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Mix Test"
        assert len(response.data["beans"]) == 2

    def test_list_mixes(self, client):

        bean = self.create_bean("Java")
        url = reverse('cofeemix-list')
        data = {
            "name": "Mix Java",
            "description": "Mix de Java",
            "beans": [{"bean_id": bean.id, "quantity": 15}]
        }
        client.post(url, data, content_type="application/json")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_mix(self, client):
        bean = self.create_bean("Robusta")
        create_url = reverse('cofeemix-list')
        data = {
            "name": "Mix Robust",
            "description": "Mix robuste avec Robusta",
            "beans": [{"bean_id": bean.id, "quantity": 30}]
        }
        create_response = client.post(create_url, data, content_type="application/json")
        mix_id = create_response.data["id"]
        detail_url = reverse('cofeemix-detail', kwargs={"pk": mix_id})
        response = client.get(detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Mix Robust"

    def test_update_mix(self, client):

        bean1 = self.create_bean("Bourbon")
        bean2 = self.create_bean("Catuai")
        create_url = reverse('cofeemix-list')
        data = {
            "name": "Mix Original",
            "description": "Description originale",
            "beans": [{"bean_id": bean1.id, "quantity": 25}]
        }
        create_response = client.post(create_url, data, content_type="application/json")
        mix_id = create_response.data["id"]
        detail_url = reverse('cofeemix-detail', kwargs={"pk": mix_id})
        update_data = {
            "name": "Mix Updated",
            "description": "Description mise à jour",
            "beans": [{"bean_id": bean2.id, "quantity": 40}]
        }
        response = client.put(detail_url, update_data, content_type="application/json")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]
        assert response.data["name"] == "Mix Updated"
        assert len(response.data["beans"]) == 1

        assert response.data["beans"][0]["bean"]["id"] == bean2.id

    def test_delete_mix(self, client):
        bean = self.create_bean("SL28")
        create_url = reverse('cofeemix-list')
        data = {
            "name": "Mix Delete",
            "description": "Mix à supprimer",
            "beans": [{"bean_id": bean.id, "quantity": 50}]
        }
        create_response = client.post(create_url, data, content_type="application/json")
        mix_id = create_response.data["id"]
        detail_url = reverse('cofeemix-detail', kwargs={"pk": mix_id})
        response = client.delete(detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = client.get(detail_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
