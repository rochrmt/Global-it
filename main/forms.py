from django import forms
from django.core.validators import FileExtensionValidator
from .models import Contact, Candidature, CandidatureSpontanee, OffreEmploi

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'telephone', 'sujet', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre téléphone'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Votre message'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_id'] = forms.IntegerField(required=False, widget=forms.HiddenInput())
        self.fields['formation_id'] = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def save(self, commit=True):
        instance = super().save(commit=False)
        service_id = self.cleaned_data.get('service_id')
        formation_id = self.cleaned_data.get('formation_id')
        
        if service_id:
            from .models import Service
            try:
                instance.service_interesse = Service.objects.get(pk=service_id)
            except Service.DoesNotExist:
                pass
                
        if formation_id:
            from .models import Formation
            try:
                instance.formation_interessee = Formation.objects.get(pk=formation_id)
            except Formation.DoesNotExist:
                pass
                
        if commit:
            instance.save()
        return instance

class QuickContactForm(forms.Form):
    nom = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'})
    )
    telephone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre téléphone'})
    )
    besoin = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre besoin'})
    )


class CandidatureForm(forms.ModelForm):
    """Formulaire de candidature pour une offre d'emploi"""
    
    class Meta:
        model = Candidature
        fields = ['nom', 'prenom', 'email', 'telephone', 'motivation', 'cv']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom',
                'required': True
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@example.com',
                'required': True
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'motivation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Expliquez vos motivations pour ce poste et vos compétences pertinentes...',
                'required': True
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'required': True
            }),
        }
    
    def clean_cv(self):
        """Validation de la taille du CV (max 5MB)"""
        cv = self.cleaned_data.get('cv')
        if cv:
            if cv.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('La taille du fichier ne doit pas dépasser 5MB.')
        return cv


class CandidatureSpontaneeForm(forms.ModelForm):
    """Formulaire de candidature spontanée"""
    
    class Meta:
        model = CandidatureSpontanee
        fields = ['nom', 'prenom', 'email', 'telephone', 'poste_souhaite', 'motivation', 'cv']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom',
                'required': True
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@example.com',
                'required': True
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'poste_souhaite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Développeur Full Stack, Chef de projet IT...',
                'required': True
            }),
            'motivation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Présentez-vous et expliquez pourquoi vous souhaitez rejoindre notre équipe...',
                'required': True
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'required': True
            }),
        }
    
    def clean_cv(self):
        """Validation de la taille du CV (max 5MB)"""
        cv = self.cleaned_data.get('cv')
        if cv:
            if cv.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('La taille du fichier ne doit pas dépasser 5MB.')
        return cv


class OffreEmploiForm(forms.ModelForm):
    """Formulaire pour créer/modifier une offre d'emploi (Admin/Dashboard)"""
    
    class Meta:
        model = OffreEmploi
        fields = [
            'titre', 'type_contrat', 'lieu', 'description', 'missions', 
            'profil_recherche', 'experience_min', 'salaire_min', 'salaire_max', 
            'date_debut', 'date_limite', 'avantages', 'image', 'urgent', 'est_actif'
        ]
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'type_contrat': forms.Select(attrs={'class': 'form-select'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'missions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profil_recherche': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'experience_min': forms.TextInput(attrs={'class': 'form-control'}),
            'salaire_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salaire_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avantages': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
