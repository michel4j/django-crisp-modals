from django.forms import Textarea
from django.urls import reverse

from crisp_modals.forms import ModalModelForm, HalfWidth, FullWidth, Row
from . import models


class PersonForm(ModalModelForm):
    class Meta:
        model = models.Person
        fields = ['first_name', 'last_name', 'age', 'bio', 'type']
        widgets = {
            'bio': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.body.title = f'Edit {self.instance.__class__.__name__}'
            self.body.form_action = reverse('person-edit', kwargs={"pk": self.instance.pk})
        self.body.append(
            Row(
                HalfWidth('first_name'), HalfWidth('last_name'),
            ),
            Row(
                HalfWidth('age'), HalfWidth('type'),
            ),
            Row(
                FullWidth('bio'),
            )
        )