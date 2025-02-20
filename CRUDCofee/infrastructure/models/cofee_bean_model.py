from django.db import models

class CofeeBeanModel(models.Model):
    """
    Modèle de persistance pour un type de grain de café.
    Correspond à l'entité CofeeBean.
    """
    name = models.CharField(max_length=100, unique=True)
    certificate_valid = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name