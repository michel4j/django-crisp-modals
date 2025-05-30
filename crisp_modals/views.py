from django.contrib.admin.utils import NestedObjects
from django.db import DEFAULT_DB_ALIAS
from django.db.models import ProtectedError
from django.http import JsonResponse, HttpRequest
from django.utils.safestring import mark_safe
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.edit import FormMixin, FormView

from .forms import ConfirmationForm


def is_ajax(request: HttpRequest) -> bool:
    """
    Check if request is an AJAX request, or prefers a JSON response
    Based on https://stackoverflow.com/questions/63629935

    :param request: HttpRequest object
    """

    return (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or request.accepts("application/json")
    )


class AjaxFormMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    modal_response = False
    success_url = ""

    def get_success_url(self):
        """
        Return the URL to redirect to after processing the form. Unlike most views, this
        URL can be blank, in which case the front-end will refresh the current page.
        """
        return self.success_url

    def form_valid(self, form):
        """
        If the request is AJAX, return a JsonResponse with the modal_response
        and the URL to redirect to. Otherwise, return the response from the
        parent class.
        """

        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if is_ajax(self.request):
            data = {
                'modal': self.modal_response,
                'url': self.get_success_url(),
            }
            return JsonResponse(data, safe=False)
        else:
            return response


class ModalUpdateView(AjaxFormMixin, UpdateView):
    """
    A Crisp Modal version of UpdateView.
    """
    template_name = 'crisp_modals/form.html'
    delete_url = None

    def get_delete_url(self):
        """
        Return the URL to delete the object, if it exists.
        """
        if self.delete_url:
            return self.delete_url
        return None


class ModalCreateView(AjaxFormMixin, CreateView):
    """
    A Crisp Modal version of CreateView.
    """
    template_name = 'crisp_modals/form.html'


class ModalFormView(AjaxFormMixin, FormView):
    """
    A Crisp Modal version of FormView
    """
    template_name = 'crisp_modals/form.html'


class ModalConfirmView(AjaxFormMixin, DeleteView):
    """
    FormView that presents a confirmation dialog and performs an action
    on confirmation.
    """
    template_name = 'crisp_modals/confirm.html'
    success_url = ""
    form_class = ConfirmationForm

    def get_form_kwargs(self):
        """
        Return the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['form_action'] = self.request.path
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.confirmed(*args, **kwargs)
        else:
            return self.form_invalid(form)

    def confirmed(self, *args, **kwargs):
        return JsonResponse({
            'message': 'Confirmed successfully',
            'url': self.get_success_url(),
        })


class ModalDeleteView(AjaxFormMixin, DeleteView):
    """
    Derived from edit.DeleteView to re-use the same get-confirm-post-execute pattern,
    Subclasses should implement 'confirmed' method
    """
    success_url = "."
    template_name = 'crisp_modals/delete.html'
    form_class = ConfirmationForm

    def get_form_kwargs(self):
        """
        Return the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['form_action'] = self.request.path
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collector = NestedObjects(using=DEFAULT_DB_ALIAS)  # database name
        collector.collect([self.object])
        related = collector.nested(delete_format)
        context['related'] = [] if len(related) == 1 else related[1]
        context['protected'] = list(collector.protected)
        return context

    def form_valid(self, form):
        return self.confirmed(self)

    def delete(self, *args, **kwargs):
        return self.confirmed(self, *args, **kwargs)

    def confirmed(self, *args, **kwargs):
        try:
            self.object.delete()
        except ProtectedError as e:
            error = 'Cannot delete this object because it is protected by other objects which reference it.'
            return JsonResponse({
                'message': error,
                'error': error,
            }, status=400)

        return JsonResponse({
            'message': 'Deleted successfully',
            'url': self.get_success_url(),
        })


def delete_format(obj):
    options = obj._meta
    return mark_safe(f"<strong>{options.verbose_name.title()}</strong> &ndash; {obj}")
