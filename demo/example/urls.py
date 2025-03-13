from django.urls import path

from . import views

urlpatterns = [
    path('people/', views.PersonList.as_view(), name='person-list'),
    path('institutions/', views.InstitutionList.as_view(), name='institution-list'),
    path('people/<int:pk>/edit/', views.PersonEdit.as_view(), name='person-edit'),
]

