from django.forms import Textarea, ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse

from crisp_modals.forms import ModalModelForm, HalfWidth, FullWidth, Row, ThirdWidth
from . import models


class PersonForm(ModalModelForm):
    class Meta:
        model = models.Person
        fields = ['first_name', 'last_name', 'age', 'bio', 'type', 'institution']
        widgets = {
            'bio': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.body.form_action = reverse('person-edit', kwargs={"pk": self.instance.pk})
        else:
            self.body.form_action = reverse('person-add')
        self.body.append(
            Row(
                ThirdWidth('first_name'), ThirdWidth('last_name'), ThirdWidth('age'),
            ),
            Row(
                HalfWidth('type'), HalfWidth('institution'),
            ),
            Row(
                FullWidth('bio'),
            )
        )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 0:
            raise ValidationError("Age cannot be negative.")
        return age

    def clean(self):
        data = super().clean()
        if data.get('age', 0) > 20 and data.get('last_name') == 'Doe':
            raise ValidationError("Persons older than 20 cannot have the last name 'Doe'.")
        return data


class InstitutionForm(ModalModelForm):
    class Meta:
        model = models.Institution
        fields = ['name', 'city', 'country', 'parent', 'subjects']
        widgets = {
            'subjects': CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.body.form_action = reverse('institution-edit', kwargs={"pk": self.instance.pk})
        else:
            self.body.form_action = reverse('institution-add')

        self.body.append(
            Row(
                HalfWidth('name'), HalfWidth('city'),
            ),
            Row(
                HalfWidth('country'), HalfWidth('parent'),
            ),
            Row(
                FullWidth('subjects'),
            )
        )


class SubjectForm(ModalModelForm):
    class Meta:
        model = models.Subject
        fields = ['name', 'description']
        widgets = {
            'description': Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.body.form_action = reverse('subject-edit', kwargs={"pk": self.instance.pk})
        else:
            self.body.form_action = reverse('subject-add')

        self.body.append(
            Row(
                FullWidth('name'),
            ),
            Row(
                FullWidth('description'),
            )
        )