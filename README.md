
django-crisp-modals
===================

django-crisp-modals is a Django app which provides support for ajax Django Crispy Forms
inside Bootstrap 5 modal dialogs.  The app provides various views, form classes, templates and 
javascript.  A demo site showcasing an example configuration various features, is available in the repository.


Quick start
-----------

1. Add "crisp_modals", and "crispy_forms" to your INSTALLED_APPS setting like this::
    ```python
    INSTALLED_APPS = [
        ...,
        "crispy_forms",
        "crispy_bootstrap5",
        "crisp_modals",
    ]
2. Add the following to your settings.py file::

    ```python
    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"

3. Include the `crisp_modals/modals.min.js` within your base template after jQuery
   and add a blank modal div to the bottom of the body tag.  The modal div should have the id: `modal-target`. 
   Then initialize the modal target.  For example:

    ```html  
    {% load static %}
    ...
    <div id="modal-target"></div>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jquery-form@4.3.0/dist/jquery.form.min.js"></script>
    <script src="{% static 'crisp_modals/modals.min.js' %}"></script>
    <script>
        $(document).ready(function() {
            $('#modal-target').initModal();
        });
    </script>
   
4. Create forms as follows. The main crispy-forms helper is available as `self.body` within the forms. 
   A footer helper is also available as `self.footer`, with submit and reset buttons already included.
   
   ```python
   from crisp_modals.forms import ModalModelForm, Row, FullWidth

    class PollForm(ModalModelForm):
         class Meta:
              model = Poll
              fields = ['question', 'pub_date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.body.form_action = reverse('polls:poll-update', kwargs={'pk': self.instance.pk})
        else:
            self.body.form_action = reverse('polls:poll-create')
        self.body.append(
            Row(
                FullWidth('question', placeholder='Enter your question'),
            ),
            Row(
                FullWidth('pub_date', placeholder='Enter the publication date'),
            )
        )

5. In your views, use the ModalCreateView, ModalUpdateView, and ModalDeleteView classes as follows. Include
   `delete_url` in the form kwargs for the ModalUpdateView class to show the delete button within the form.
    
    ```python
    from crisp_modals.views import ModalCreateView, ModalUpdateView, ModalDeleteView

    class PollCreateView(ModalCreateView):
        model = Poll
        form_class = PollForm

    class PollCreateView(ModalUpdateView):
        model = Poll
        form_class = PollForm
        
        def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['delete_url'] = reverse('polls:poll-delete', kwargs={'pk': self.object.pk})
            return kwargs
   
    class PollDeleteView(ModalDeleteView):
        model = Poll
   

    
6. To distinguish regular links from links that target modals, use the 'data-modal-url' attribute instead of href.
   For example:

    ```html
    <a href="#0" data-modal-url="{% url 'polls:poll-create' %}" class="modal-link">Create Poll</a>
    <a href="#0" data-modal-url="{% url 'polls:poll-update' pk=poll.pk %}">Update Poll</a>

> Note: 
> 
> The `data-modal-url` attribute should contain the url of the view that will render the modal. It doesn't have to 
> return a form. Non-form modal content can be rendered by overriding the `modal_content` block in the modal template
> `crisp_modals/modal.html`.  The following blocks are available for overriding: `modal_header`, `modal_body`, `modal_footer`,
> `modal_scripts`.  The `modal_scripts` block should be used to include any additional javascript required for the modal 
> content.