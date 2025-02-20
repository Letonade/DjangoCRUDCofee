from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.cofee_bean_view_set import CofeeBeanViewSet
from .views.cofee_mix_view_set import CofeeMixViewSet

router = DefaultRouter()
router.register(r'beans', CofeeBeanViewSet, basename='cofeebean')
router.register(r'mixes', CofeeMixViewSet, basename='cofeemix')

urlpatterns = [
    path('', include(router.urls)),
]

# GET /api/beans/ : Lister tous les grains de café.
# POST /api/beans/ : Créer un nouveau grain de café.
# GET /api/beans/{id}/ : Afficher les détails d'un grain de café.
# PUT/PATCH /api/beans/{id}/ : Modifier un grain de café. ignore certificate_valid (false par défaut)
# DELETE /api/beans/{id}/ : Supprimer un grain de café.
# POST /api/beans/{id}/toggle_certificate/ : inverser la valeur certificate_valid

# GET /api/mixes/ : Lister tous les mixes.
# POST /api/mixes/ : Créer un nouveau mix.
#   Le corps de la requête devra inclure des informations pour le mix (nom, description) ainsi qu'une liste d'entrées
#   sous la clé beans (chaque entrée comprenant bean_id et quantity).
#{
# "name": "Mix Fruité",
# "description": "Un mélange équilibré avec des notes fruitées",
# "beans": [
#     {
#         "bean_id": 1,
#         "quantity": 10
#     },
#     {
#         "bean_id": 2,
#         "quantity": 20
#     }
#]
#}
# GET /api/mixes/{id}/ : Récupérer les détails d'un mix.
# PUT/PATCH /api/mixes/{id}/ : Mettre à jour un mix.