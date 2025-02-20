from django.db import models
from .cofee_bean_model import CofeeBeanModel

class CofeeMixModel(models.Model):
    """
    Modèle de persistance pour un mixage de café.
    Correspond à l'entité CofeeMix.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    beans = models.ManyToManyField(CofeeBeanModel, through='CofeeMixEntryModel')

    def __str__(self):
        return self.name


class CofeeMixEntryModel(models.Model):
    """
    Modèle intermédiaire pour représenter l'association entre un mix (CofeeMixModel)
    et un bean (CofeeBeanModel) avec une quantité spécifique (en grammes).
    Correspond à l'association définie par CofeeMixEntry dans le domaine.
    """
    mix = models.ForeignKey(CofeeMixModel, on_delete=models.CASCADE)
    bean = models.ForeignKey(CofeeBeanModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Quantité en grammes")

    class Meta:
        unique_together = ('mix', 'bean')

    def __str__(self):
        return f"{self.quantity}g de {self.bean.name} dans {self.mix.name}"
