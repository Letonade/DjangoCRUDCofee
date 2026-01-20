#!/usr/bin/env python
"""
Usage :
    python mdata.py fill
        Remplit la base de données avec 10 types de grains de café différents
        et quelques mix pour illustrer toutes les possibilités.

    python mdata.py see
        Affiche dans la console l'ensemble des grains de café et des mix enregistrés.
"""

import sys
import os
import django

# Configuration de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoCRUDCofee.settings")
django.setup()

from CRUDCofee.models import CofeeBeanModel, CofeeMixModel, CofeeMixEntryModel

def fill_database():
    CofeeMixEntryModel.objects.all().delete()
    CofeeMixModel.objects.all().delete()
    CofeeBeanModel.objects.all().delete()

    beans_data = [
        {"name": "Arabica", "certificate_valid": True,  "description": "Grain de café Arabica de haute qualité"},
        {"name": "Moka",    "certificate_valid": True,  "description": "Grain de café Moka au goût unique"},
        {"name": "Java",    "certificate_valid": False, "description": "Café Java robuste"},
        {"name": "Robusta", "certificate_valid": True,  "description": "Grain de café Robusta, plus corsé"},
        {"name": "Liberica","certificate_valid": False, "description": "Café rare, typiquement de Liberica"},
        {"name": "Excelsa", "certificate_valid": True,  "description": "Grain d'Excelsa, offrant une complexité aromatique"},
        {"name": "Typica",  "certificate_valid": True,  "description": "Café Typica, la base de nombreux mélanges"},
        {"name": "Bourbon", "certificate_valid": True,  "description": "Grain Bourbon, doux et fruité"},
        {"name": "Catuai",  "certificate_valid": False, "description": "Catuai, robuste et équilibré"},
        {"name": "SL28",    "certificate_valid": True,  "description": "Café SL28, apprécié pour son acidulé"}
    ]

    bean_models = {}
    for bean in beans_data:
        bean_model = CofeeBeanModel.objects.create(**bean)
        bean_models[bean["name"]] = bean_model
        print(f"Création du bean : {bean['name']}")

    # Mix 1 : 20g d'Arabica, 10g de Moka
    mix1 = CofeeMixModel.objects.create(name="Mix doux", description="Mix équilibré avec une dominance d'Arabica")
    CofeeMixEntryModel.objects.create(mix=mix1, bean=bean_models["Arabica"], quantity=20)
    CofeeMixEntryModel.objects.create(mix=mix1, bean=bean_models["Moka"], quantity=10)
    print("Création du mix : Mix doux")

    # Mix 2 : 15g de Java, 15g de Robusta
    mix2 = CofeeMixModel.objects.create(name="Mix corsé", description="Mix puissant pour les amateurs de café fort")
    CofeeMixEntryModel.objects.create(mix=mix2, bean=bean_models["Java"], quantity=15)
    CofeeMixEntryModel.objects.create(mix=mix2, bean=bean_models["Robusta"], quantity=15)
    print("Création du mix : Mix corsé")

    # Mix 3 : 10g d'Arabica, 10g de Bourbon, 10g de SL28
    mix3 = CofeeMixModel.objects.create(name="Mix fruité", description="Mélange équilibré avec des notes fruitées")
    CofeeMixEntryModel.objects.create(mix=mix3, bean=bean_models["Arabica"], quantity=10)
    CofeeMixEntryModel.objects.create(mix=mix3, bean=bean_models["Bourbon"], quantity=10)
    CofeeMixEntryModel.objects.create(mix=mix3, bean=bean_models["SL28"], quantity=10)
    print("Création du mix : Mix fruité")

    print("Base de données remplie avec succès.")


def see_database():
    print("=== Grains de Café ===")
    beans = CofeeBeanModel.objects.all()
    if not beans:
        print("Aucun bean trouvé.")
    else:
        for bean in beans:
            print(f"ID: {bean.id} | Nom: {bean.name} | Certificat valide: {bean.certificate_valid} | Description: {bean.description}")

    print("\n=== Mix de Café ===")
    mixes = CofeeMixModel.objects.all()
    if not mixes:
        print("Aucun mix trouvé.")
    else:
        for mix in mixes:
            print(f"ID: {mix.id} | Nom: {mix.name} | Description: {mix.description}")
            entries = mix.cofeemixentrymodel_set.all()  # l'accès via le reverse relation
            if entries:
                for entry in entries:
                    print(f"  - {entry.quantity}g de {entry.bean.name}")
            else:
                print("  Aucun bean associé.")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["fill", "see"]:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]
    if action == "fill":
        fill_database()
    elif action == "see":
        see_database()


if __name__ == "__main__":
    main()
