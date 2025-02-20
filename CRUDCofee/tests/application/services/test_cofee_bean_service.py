import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCRUDCofee.settings')
django.setup()

import pytest
from CRUDCofee.application.services.cofee_bean_service import CofeeBeanService
from CRUDCofee.models import CofeeBeanModel

@pytest.mark.django_db
class TestCofeeBeanService:
    @pytest.fixture(autouse=True)
    def setup_service(self):
        self.service = CofeeBeanService()

    def test_add_and_get(self):
        bean_model = self.service.add_cofee_bean(
            name="Arabica",
            certificate_valid=True,
            description="Grain premium"
        )

        fetched = self.service.get_cofee_bean(bean_model.id)
        assert fetched.name == "Arabica"
        assert fetched.certificate_valid is True
        assert fetched.description == "Grain premium"

    def test_update(self):
        # Création d'un bean initial
        bean_model = self.service.add_cofee_bean(
            name="Moka",
            certificate_valid=False,
            description="Description initiale"
        )

        updated_model = self.service.update_cofee_bean(
            bean_model.id,
            name="Moka Updated",
            certificate_valid=True
        )
        assert updated_model.name == "Moka Updated"
        assert updated_model.certificate_valid is True

        assert updated_model.description == "Description initiale"

    def test_delete(self):
        bean_model = self.service.add_cofee_bean(
            name="Java",
            certificate_valid=True,
            description="Description Java"
        )
        bean_id = bean_model.id

        self.service.delete_cofee_bean(bean_id)
        with pytest.raises(CofeeBeanModel.DoesNotExist):
            self.service.get_cofee_bean(bean_id)

    def test_list_all(self):
        assert self.service.list_cofee_beans().count() == 0

        self.service.add_cofee_bean("Arabica", True, "desc 1")
        self.service.add_cofee_bean("Moka", False, "desc 2")

        assert self.service.list_cofee_beans().count() == 2
