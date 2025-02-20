import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoCRUDCofee.settings')
django.setup()

import pytest
from CRUDCofee.models import CofeeBeanModel, CofeeMixModel
from CRUDCofee.application.services.cofee_mix_service import CofeeMixService

@pytest.mark.django_db
class TestCofeeMixService:
    def create_bean(self, name: str) -> CofeeBeanModel:
        return CofeeBeanModel.objects.create(
            name=name,
            certificate_valid=True,
            description=f"Description pour {name}"
        )

    def test_add_and_get(self):
        service = CofeeMixService()
        bean1 = self.create_bean("Arabica")
        bean2 = self.create_bean("Moka")
        mix = service.add_cofee_mix(
            name="Service Mix",
            description="Mix créé par le service",
            beans=[{"bean_id": bean1.id, "quantity": 30}, {"bean_id": bean2.id, "quantity": 15}]
        )
        assert mix.name == "Service Mix"
        retrieved = service.get_cofee_mix(mix.id)
        assert retrieved.name == "Service Mix"
        entries = retrieved.cofeemixentrymodel_set.all()
        assert entries.count() == 2

    def test_update(self):
        service = CofeeMixService()
        bean1 = self.create_bean("Java")
        bean2 = self.create_bean("Robusta")
        mix = service.add_cofee_mix(
            name="Initial Service Mix",
            description="Mix initial",
            beans=[{"bean_id": bean1.id, "quantity": 15}]
        )
        updated_mix = service.update_cofee_mix(
            mix_id=mix.id,
            name="Updated Service Mix",
            description="Mix mis à jour",
            beans=[{"bean_id": bean2.id, "quantity": 40}]
        )
        assert updated_mix.name == "Updated Service Mix"
        entries = updated_mix.cofeemixentrymodel_set.all()
        assert entries.count() == 1
        entry = entries.first()
        assert entry.bean.id == bean2.id
        assert entry.quantity == 40

    def test_delete(self):
        service = CofeeMixService()
        bean = self.create_bean("SL28")
        mix = service.add_cofee_mix(
            name="Service Mix Delete",
            description="Mix à supprimer",
            beans=[{"bean_id": bean.id, "quantity": 50}]
        )
        mix_id = mix.id
        service.delete_cofee_mix(mix_id)
        with pytest.raises(CofeeMixModel.DoesNotExist):
            service.get_cofee_mix(mix_id)

    def test_list_all(self):
        service = CofeeMixService()
        bean = self.create_bean("Typica")
        initial_count = service.list_cofee_mixes().count()
        service.add_cofee_mix(name="Mix A", description="Desc A", beans=[{"bean_id": bean.id, "quantity": 20}])
        service.add_cofee_mix(name="Mix B", description="Desc B", beans=[{"bean_id": bean.id, "quantity": 30}])
        assert service.list_cofee_mixes().count() == initial_count + 2
