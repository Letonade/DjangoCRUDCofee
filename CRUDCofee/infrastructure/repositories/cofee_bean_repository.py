from CRUDCofee.infrastructure.models import CofeeBeanModel
from CRUDCofee.domain.entities.cofeeBean import CofeeBean

class CofeeBeanRepository:
    """
    Repository pour gérer la persistance des instances de CofeeBean.
    """

    def add(self, bean: CofeeBean) -> CofeeBeanModel:
        bean_model = CofeeBeanModel.objects.create(
            name=bean.name,
            certificate_valid=bean.certificate_valid,
            description=bean.description
        )
        return bean_model

    def get(self, bean_id: int) -> CofeeBeanModel:
        return CofeeBeanModel.objects.get(pk=bean_id)

    def update(self, bean_id: int, **kwargs) -> CofeeBeanModel:
        bean_model = self.get(bean_id)
        for key, value in kwargs.items():
            setattr(bean_model, key, value)
        bean_model.save()
        return bean_model

    def delete(self, bean_id: int) -> None:
        bean_model = self.get(bean_id)
        bean_model.delete()

    def list_all(self):
        return CofeeBeanModel.objects.all()
