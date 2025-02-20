from CRUDCofee.models import CofeeMixModel, CofeeMixEntryModel, CofeeBeanModel

class CofeeMixRepository:
    """
    Repository pour gérer la persistance des mixes de café et de leurs entrées associées.
    """

    def add(self, name: str, description: str, beans: list):
        """
        Crée un nouveau mix ainsi que ses entrées associées.

        Args:
            name (str): Le nom du mix.
            description (str): La description du mix.
            beans (list): Une liste de dictionnaires, chacun contenant :
                          - "bean_id": L'ID du bean (CofeeBeanModel)
                          - "quantity": La quantité en grammes pour ce bean dans le mix.

        Returns:
            CofeeMixModel: L'instance du mix créé.
        """
        mix = CofeeMixModel.objects.create(name=name, description=description)
        for entry in beans:
            # On récupère le bean correspondant via son ID.
            bean = CofeeBeanModel.objects.get(pk=entry["bean_id"])
            CofeeMixEntryModel.objects.create(mix=mix, bean=bean, quantity=entry["quantity"])
        return mix

    def get(self, mix_id: int):
        """
        Récupère un mix par son ID.
        """
        return CofeeMixModel.objects.get(pk=mix_id)

    def update(self, mix_id: int, name: str = None, description: str = None, beans: list = None):
        """
        Met à jour un mix existant.

        Args:
            mix_id (int): L'identifiant du mix.
            name (str, optionnel): Nouveau nom du mix.
            description (str, optionnel): Nouvelle description.
            beans (list, optionnel): Nouvelle liste d'entrées pour le mix (format identique à add).

        Returns:
            CofeeMixModel: L'instance mise à jour du mix.
        """
        mix = self.get(mix_id)
        if name is not None:
            mix.name = name
        if description is not None:
            mix.description = description
        mix.save()

        if beans is not None:
            # On remplace toutes les entrées existantes par celles fournies.
            mix.cofeemixentrymodel_set.all().delete()
            for entry in beans:
                bean = CofeeBeanModel.objects.get(pk=entry["bean_id"])
                CofeeMixEntryModel.objects.create(mix=mix, bean=bean, quantity=entry["quantity"])
        return mix

    def delete(self, mix_id: int):
        """
        Supprime le mix identifié par mix_id.
        """
        mix = self.get(mix_id)
        mix.delete()

    def list_all(self):
        """
        Retourne la liste de tous les mixes.
        """
        return CofeeMixModel.objects.all()
