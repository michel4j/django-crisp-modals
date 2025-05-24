from django.urls import reverse
from django.views.generic import ListView, TemplateView
from crisp_modals.views import ModalUpdateView, ModalCreateView, ModalDeleteView, ModalConfirmView
from demo.example.forms import PersonForm, InstitutionForm, SubjectForm
from demo.example.models import Person, Institution, Subject


# Create your views here.
class PersonList(ListView):
    model = Person
    template_name = 'example/person_list.html'
    paginate_by = 15


class InstitutionList(ListView):
    model = Institution
    template_name = 'example/institution_list.html'
    paginate_by = 15


class SubjectList(ListView):
    model = Subject
    template_name = 'example/subject_list.html'
    paginate_by = 15


class EditPerson(ModalUpdateView):
    model = Person
    form_class = PersonForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['delete_url'] = reverse('person-delete', kwargs={'pk': self.object.pk})
        return kwargs


class AddPerson(ModalCreateView):
    model = Person
    form_class = PersonForm


class EditInstitution(ModalUpdateView):
    model = Institution
    form_class = InstitutionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['delete_url'] = reverse('institution-delete', kwargs={'pk': self.object.pk})
        return kwargs


class AddInstitution(ModalCreateView):
    model = Institution
    form_class = InstitutionForm


class EditSubject(ModalUpdateView):
    model = Subject
    form_class = SubjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['delete_url'] = reverse('subject-delete', kwargs={'pk': self.object.pk})
        return kwargs


class AddSubject(ModalCreateView):
    model = Subject
    form_class = SubjectForm


class DeletePerson(ModalConfirmView):
    model = Person


class DeleteInstitution(ModalDeleteView):
    model = Institution


class DeleteSubject(ModalDeleteView):
    model = Subject


class HomeView(TemplateView):
    template_name = "example/home.html"

