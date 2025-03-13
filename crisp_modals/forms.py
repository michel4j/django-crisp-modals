from crispy_forms.bootstrap import StrictButton, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms
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
    def __init__(self, form):
        super().__init__(form)
        #self.disable_csrf = True
        self.append(
            Button('Revert', type='reset', value='Reset', style="btn-secondary"),
            Button('Save', type='submit', name='submit', value='submit', style='btn-primary'),
        )


class ModalModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = BodyHelper(self)
        self.footer = FooterHelper(self)


class ModalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = BodyHelper(self)
        self.footer = FooterHelper(self)