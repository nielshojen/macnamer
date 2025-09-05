from django import forms
from .models import *

class ComputerGroupForm(forms.ModelForm):
    class Meta:
        model = ComputerGroup
        fields = ('name','prefix','divider','domain',)

class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = ('name','serial',)
        
class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ('network',)

class APIKeyCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    expires_at = forms.DateTimeField(
        required=False,
        help_text="Optional",
        widget=forms.TextInput(attrs={"placeholder": "2025-12-31 23:59"})
    )