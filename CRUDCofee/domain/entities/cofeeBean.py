from dataclasses import dataclass

@dataclass(frozen=True)
class CofeeBean:
    """
    Représente un type de grain de café.

    Attributs :
      - name: Nom du grain (ex: "Arabica", "Moka", "Java").
      - certificate_valid: Booléen indiquant la validité du certificat de provenance.
      - description: Description textuelle du grain.
    """
    name: str
    certificate_valid: bool
    description: str
