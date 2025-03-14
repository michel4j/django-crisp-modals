from django.contrib.admin.utils import NestedObjects
from django.db import DEFAULT_DB_ALIAS
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.generic import UpdateView, CreateView, DeleteView


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
    UpdateView that returns a JsonResponse if the request is AJAX.
    """
    template_name = 'django_crisp_modals/form.html'


class ModalCreateView(AjaxFormMixin, CreateView):
    """
    CreateView that returns a JsonResponse if the request is AJAX.
    """
    template_name = 'django_crisp_modals/form.html'


class ModalDeleteView(AjaxFormMixin, DeleteView):
    """derived from edit.DeleteView to re-use the same get-confirm-post-execute pattern
    Sub-classes should implement 'confirmed' method
    """

    template_name = 'django_crisp_modals/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collector = NestedObjects(using=DEFAULT_DB_ALIAS)  # database name
        collector.collect([context['object']])  # list of objects. single one won't do
        context['related'] = collector.nested(delete_format)
        return context

    def form_valid(self, form):
        return self.confirmed(self)

    def delete(self, *args, **kwargs):
        return self.confirmed(self, *args, **kwargs)

    def confirmed(self, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())


def delete_format(obj):
    return f"{obj._meta.verbose_name}: {obj}"