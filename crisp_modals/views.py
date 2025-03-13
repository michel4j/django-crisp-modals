from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest


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

