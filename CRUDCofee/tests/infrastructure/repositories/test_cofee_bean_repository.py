import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCRUDCofee.settings')
django.setup()

import pytest
from CRUDCofee.infrastructure.repositories.cofee_bean_repository import CofeeBeanRepository
from CRUDCofee.infrastructure.models.cofee_bean_model import CofeeBeanModel
from CRUDCofee.domain.entities.cofeeBean import CofeeBean

# given, when, then
@pytest.mark.django_db
class TestCofeeBeanRepository:
    @pytest.fixture(autouse=True)
    def setup_repo(self):
        self.repo = CofeeBeanRepository()

    def test_add_and_get(self):
        bean = CofeeBean(name="Arabica", certificate_valid=True, description="Grain premium")
        bean_model = self.repo.add(bean)

        fetched = self.repo.get(bean_model.id)
        assert fetched.name == "Arabica"
        assert fetched.certificate_valid is True
        assert fetched.description == "Grain premium"

    def test_update(self):
        bean = CofeeBean(name="Moka", certificate_valid=False, description="Description initiale")
        bean_model = self.repo.add(bean)

        updated_model = self.repo.update(bean_model.id, name="Moka Updated", certificate_valid=True)
        assert updated_model.name == "Moka Updated"
        assert updated_model.certificate_valid is True
        assert updated_model.description == "Description initiale"

    def test_delete(self):
        bean = CofeeBean(name="Java", certificate_valid=True, description="Description Java")
        bean_model = self.repo.add(bean)
        bean_id = bean_model.id

        self.repo.delete(bean_id)
        with pytest.raises(CofeeBeanModel.DoesNotExist):
            self.repo.get(bean_id)

    def test_list_all(self):
        assert self.repo.list_all().count() == 0

        bean1 = CofeeBean(name="Arabica", certificate_valid=True, description="desc 1")
        bean2 = CofeeBean(name="Moka", certificate_valid=False, description="desc 2")
        self.repo.add(bean1)
        self.repo.add(bean2)

        assert self.repo.list_all().count() == 2
