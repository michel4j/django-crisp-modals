from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from crisp_modals.views import ModalUpdateView, ModalCreateView
from demo.example.forms import PersonForm
from demo.example.models import Person, Institution


# Create your views here.
class PersonList(ListView):
    model = Person
    template_name = 'example/person_list.html'
    paginate_by = 15


class InstitutionList(ListView):
    model = Institution
    template_name = 'example/person_list.html'
    paginate_by = 15


class PersonEdit(ModalUpdateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person-list')

