import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCRUDCofee.settings')
django.setup()

import pytest
from CRUDCofee.models import CofeeBeanModel, CofeeMixModel, CofeeMixEntryModel
from CRUDCofee.infrastructure.repositories.cofee_mix_repository import CofeeMixRepository

@pytest.mark.django_db
class TestCofeeMixRepository:
    def create_bean(self, name: str) -> CofeeBeanModel:
        return CofeeBeanModel.objects.create(
            name=name,
            certificate_valid=True,
            description=f"Description pour {name}"
        )

    def test_add_and_get(self):
        repo = CofeeMixRepository()
        bean1 = self.create_bean("Arabica")
        bean2 = self.create_bean("Moka")

        mix = repo.add(
            name="Test Mix",
            description="Mix de test avec Arabica et Moka",
            beans=[{"bean_id": bean1.id, "quantity": 20}, {"bean_id": bean2.id, "quantity": 10}]
        )
        assert mix.name == "Test Mix"
        # Récupération via le repository
        retrieved = repo.get(mix.id)
        assert retrieved.name == "Test Mix"
        entries = retrieved.cofeemixentrymodel_set.all()
        assert entries.count() == 2

    def test_update(self):
        repo = CofeeMixRepository()
        bean1 = self.create_bean("Java")
        bean2 = self.create_bean("Robusta")
        mix = repo.add(
            name="Initial Mix",
            description="Description initiale",
            beans=[{"bean_id": bean1.id, "quantity": 15}]
        )
        updated_mix = repo.update(
            mix_id=mix.id,
            name="Updated Mix",
            description="Description mise à jour",
            beans=[{"bean_id": bean2.id, "quantity": 25}]
        )
        assert updated_mix.name == "Updated Mix"
        entries = updated_mix.cofeemixentrymodel_set.all()
        assert entries.count() == 1
        entry = entries.first()
        assert entry.bean.id == bean2.id
        assert entry.quantity == 25

    def test_delete(self):
        repo = CofeeMixRepository()
        bean = self.create_bean("Liberica")
        mix = repo.add(
            name="Mix to Delete",
            description="Mix à supprimer",
            beans=[{"bean_id": bean.id, "quantity": 30}]
        )
        mix_id = mix.id
        repo.delete(mix_id)
        with pytest.raises(CofeeMixModel.DoesNotExist):
            repo.get(mix_id)

    def test_list_all(self):
        repo = CofeeMixRepository()
        bean = self.create_bean("Excelsa")
        initial_count = repo.list_all().count()
        repo.add(name="Mix1", description="Desc 1", beans=[{"bean_id": bean.id, "quantity": 10}])
        repo.add(name="Mix2", description="Desc 2", beans=[{"bean_id": bean.id, "quantity": 20}])
        assert repo.list_all().count() == initial_count + 2
