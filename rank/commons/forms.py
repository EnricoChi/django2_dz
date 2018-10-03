from django import forms


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.fields.BooleanField):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
