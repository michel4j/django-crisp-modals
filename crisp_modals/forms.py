from crispy_forms.bootstrap import StrictButton, AppendedText, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe


class Row(Div):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"row {style}", **kwargs)


class FillWidth(Div):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"col {style}", **kwargs)


class FullWidth(Div):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"col-12 {style}", **kwargs)


class HalfWidth(Div):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"col-6 {style}", **kwargs)


class ThirdWidth(Div):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"col-4 {style}", **kwargs)


class QuarterWidth(Div):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"col-3 {style}", **kwargs)


class SixthWidth(Div):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"col-2 {style}", **kwargs)


class Button(StrictButton):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"btn {style}", **kwargs)


class IconEntry(AppendedText):
    def __init__(self, name, icon="",  style="", **kwargs):
        super().__init__(name, mark_safe(f'<i class="{icon}"></i>'), css_class=style, **kwargs)


class BodyHelper(FormHelper):
    def __init__(self, form):
        super().__init__(form)
        self.form_tag = False
        self.title = 'Form'
        self.form_show_errors = False
        self.layout = Layout()

    def append(self, *args):
        self.layout.extend(args)


class FooterHelper(BodyHelper):
    def __init__(self, form, delete_url=None):
        super().__init__(form)
        buttons = []
        if delete_url:
            buttons.append(
                Button('Delete', id="delete-object", style="btn-danger me-auto", data_modal_url=delete_url)
            )
        buttons.extend([
            Button('Revert', type='reset', value='Reset', style="btn-secondary"),
            Button('Save', type='submit', name='submit', value='submit', style='btn-primary'),
        ])
        self.append(*buttons)


class ModalModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.delete_url = kwargs.pop('delete_url', None)
        super().__init__(*args, **kwargs)
        self.body = BodyHelper(self)
        self.footer = FooterHelper(self, delete_url=self.delete_url)
        if self.instance.pk:
            self.body.title = f'Edit {self.instance.__class__.__name__}'
        else:
            self.body.title = f'Add {self.Meta.model.__name__}'


class ModalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = BodyHelper(self)
        self.footer = FooterHelper(self)
