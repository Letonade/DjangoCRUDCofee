from CRUDCofee.domain.entities.cofeeBean import CofeeBean
from CRUDCofee.infrastructure.repositories.cofee_bean_repository import CofeeBeanRepository

class CofeeBeanService:
    """
    Service pour gérer les opérations sur les grains de café (CofeeBean).
    """

    def __init__(self, repository: CofeeBeanRepository = None):
        self.repository = repository or CofeeBeanRepository()

    def add_cofee_bean(self, name: str, certificate_valid: bool, description: str):
        bean = CofeeBean(name=name, certificate_valid=certificate_valid, description=description)
        return self.repository.add(bean)

    def get_cofee_bean(self, bean_id: int):
        return self.repository.get(bean_id)

    def update_cofee_bean(self, bean_id: int, **kwargs):
        return self.repository.update(bean_id, **kwargs)

    def delete_cofee_bean(self, bean_id: int):
        self.repository.delete(bean_id)

    def list_cofee_beans(self):
        return self.repository.list_all()
