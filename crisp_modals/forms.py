from crispy_forms.bootstrap import StrictButton, AppendedText, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe


class Row(Div):
    """
    A row of form widgets.
    """
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"row {style}", **kwargs)


class FillWidth(Div):
    width_class = "col-auto"

    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"{self.width_class} {style}", **kwargs)


class FullWidth(FillWidth):
    width_class = "col-12"


class HalfWidth(FillWidth):
    width_class = "col-6"


class ThirdWidth(FillWidth):
    width_class = "col-4"


class QuarterWidth(FillWidth):
    width_class = "col-3"


class SixthWidth(FillWidth):
    width_class = "col-2"


class TwoThirdWidth(FillWidth):
    width_class = "col-8"


class ThreeQuarterWidth(FillWidth):
    width_class = "col-9"


class FiveSixthWidth(FillWidth):
    width_class = "col-10"


class Button(StrictButton):
    def __init__(self, *args,  style="", **kwargs):
        super().__init__(*args, css_class=f"btn {style}", **kwargs)


class IconEntry(AppendedText):
    def __init__(self, name, icon="",  style="", **kwargs):
        super().__init__(name, mark_safe(f'<i class="{icon}"></i>'), css_class=style, **kwargs)


class BodyHelper(FormHelper):
    """
    A crispy form helper for the body of the form.
    """

    def __init__(self, form):
        super().__init__(form)
        self.form_tag = False
        self.title = 'Form'
        self.method = 'POST'
        self.form_show_errors = False
        self.layout = Layout()

    def append(self, *args):
        """
        Append layout objects to the layout.
        """
        self.layout.extend(args)


class FooterHelper(BodyHelper):
    """
    A crispy form helper for the footer of a modal, with action buttons.
    """
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
        self.set_buttons(*buttons)

    def set_buttons(self, *buttons: Button):
        """
        Set the footer buttons for the modal form.
        :param buttons: Button instances to be added to the footer. Any Crispy layout objects can be added.
        """
        self.layout = Layout(*buttons)


class ModalModelForm(forms.ModelForm):
    """
    A ModelForm that is used in a modal. It uses crispy forms to render the form.
    """

    def __init__(self, *args, delete_url=None, form_action=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = BodyHelper(self)
        if form_action:
            self.body.form_action = form_action
        self.footer = FooterHelper(self, delete_url=delete_url)
        if self.instance.pk:
            self.body.title = f'Edit {self.instance.__class__.__name__}'
        else:
            self.body.title = f'Add {self.Meta.model.__name__}'


class ModalForm(forms.Form):
    """
    A Form that is used in a modal. It uses crispy forms to render the form.
    """

    def __init__(self, *args, form_action=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = BodyHelper(self)
        if form_action:
            self.body.form_action = form_action
        self.footer = FooterHelper(self)


class ConfirmationForm(ModalForm):
    """
    A Form that is used in a modal to confirm an action. It uses crispy forms to render the form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body.title = 'Confirmation'
        self.footer.set_buttons(
            Button('Cancel', type='button', value='cancel', style="btn-secondary", data_bs_dismiss="modal"),
            Button("Yes", type='submit', name='confirm', value='confirm', style='btn-danger'),
        )
