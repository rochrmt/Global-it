from django import forms
from main.models import Partner

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['nom', 'site_web', 'logo', 'description', 'ordre', 'est_actif']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field_name == 'logo':
                field.widget.attrs.update({'class': 'form-control'})
            elif field_name == 'description':
                field.widget.attrs.update({'class': 'form-control', 'rows': 3})
            elif field_name == 'est_actif':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})