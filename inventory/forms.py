from django import forms

from .models import Component


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ("name", "value", "description", "quantity", "location")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Resistor"}),
            "value": forms.TextInput(attrs={"placeholder": "e.g. 10kΩ"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Optional notes about this component", "rows": 3}
            ),
            "quantity": forms.NumberInput(attrs={"min": 0}),
            "location": forms.TextInput(attrs={"placeholder": "e.g. Drawer A3"}),
        }
