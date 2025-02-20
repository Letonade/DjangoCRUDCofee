from dataclasses import dataclass, field
from typing import List
from .cofeeBean import CofeeBean

@dataclass(frozen=True)
class CofeeMixEntry:
    """
    Représente une association d'un type de grain (CofeeBean) à une quantité spécifique (en grammes)
    dans un mix.

    Attributs :
      - bean: Instance de CofeeBean.
      - quantity: Quantité en grammes de ce bean dans le mix.
    """
    bean: CofeeBean
    quantity: int

@dataclass(frozen=True)
class CofeeMix:
    """
    Représente un mixage de café composé de différentes associations de grains et de quantités.

    Attributs :
      - name: Nom du mixage.
      - beans: Liste des associations (CofeeMixEntry) définissant la composition du mix.
      - description: Description textuelle du mixage.
    """
    name: str
    beans: List[CofeeMixEntry] = field(default_factory=list)
    description: str = ""
