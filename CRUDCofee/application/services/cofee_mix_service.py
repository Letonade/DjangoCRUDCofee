from CRUDCofee.domain.entities.cofeeMix import CofeeMix, CofeeMixEntry
from CRUDCofee.infrastructure.repositories.cofee_mix_repository import CofeeMixRepository

class CofeeMixService:
    """
    Service pour gérer les opérations sur les mixes de café.
    
    Fournit des méthodes pour ajouter, récupérer, mettre à jour, supprimer 
    et lister les mixes en utilisant le repository associé.
    """

    def __init__(self, repository: CofeeMixRepository = None):
        self.repository = repository or CofeeMixRepository()

    def add_cofee_mix(self, name: str, description: str, beans: list):
        """
        Ajoute un nouveau mix de café.
        
        Args:
            name (str): Le nom du mix.
            description (str): La description du mix.
            beans (list): Une liste de dictionnaires pour chaque entrée du mix.
                Chaque dictionnaire doit contenir les clés :
                    - "bean_id" : l'identifiant du grain de café (CofeeBeanModel) à inclure
                    - "quantity" : la quantité en grammes pour ce bean

        Returns:
            L'instance du mix créé (généralement le modèle persistant).
        """
        return self.repository.add(name, description, beans)

    def get_cofee_mix(self, mix_id: int):
        """
        Récupère un mix de café par son ID.
        """
        return self.repository.get(mix_id)

    def update_cofee_mix(self, mix_id: int, name: str = None, description: str = None, beans: list = None):
        """
        Met à jour un mix existant. Les paramètres facultatifs permettent
        de modifier le nom, la description et/ou la composition (les beans).
        
        Args:
            mix_id (int): L'identifiant du mix.
            name (str, optionnel): Nouveau nom du mix.
            description (str, optionnel): Nouvelle description.
            beans (list, optionnel): Nouvelle liste d'entrées de mix (format identique à add_cofee_mix).

        Returns:
            L'instance mise à jour du mix.
        """
        return self.repository.update(mix_id, name=name, description=description, beans=beans)

    def delete_cofee_mix(self, mix_id: int):
        """
        Supprime le mix de café identifié par mix_id.
        """
        self.repository.delete(mix_id)

    def list_cofee_mixes(self):
        """
        Renvoie la liste de tous les mixes enregistrés.
        """
        return self.repository.list_all()
