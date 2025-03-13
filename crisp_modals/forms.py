from crispy_forms.bootstrap import StrictButton, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms
from django.utils.safestring import mark_safe


class Row(Div):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"row {styles}", **kwargs)


class FillWidth(Div):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"col {styles}", **kwargs)


class FullWidth(Div):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"col-12 {styles}", **kwargs)


class HalfWidth(Div):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"col-6 {styles}", **kwargs)


class ThirdWidth(Div):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"col-4 {styles}", **kwargs)


class QuarterWidth(Div):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"col-3 {styles}", **kwargs)


class SixthWidth(Div):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"col-2 {styles}", **kwargs)


class Button(StrictButton):
    def __init__(self, styles="", *args, **kwargs):
        super().__init__(*args, css_class=f"btn {styles}", **kwargs)


class IconEntry(AppendedText):
    def __init__(self, name, icon="",  styles="", **kwargs):
        super().__init__(name, mark_safe(f'<i class="{icon}"></i>'), css_class=styles, **kwargs)


class BodyHelper(FormHelper):
    def __init__(self, form):
        super().__init__(form)
        self.form_tag = False
        self.form_show_errors = False
        self.layout = Layout()

    def append(self, *args):
        self.layout.extend(*args)


class FooterHelper(BodyHelper):
    def __init__(self, form):
        super().__init__(form)
        self.disable_csrf = True


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