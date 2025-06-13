from django import forms
from .models import Pet, JobRequest


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'notes', 'photo']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            "name": "Nombre",
            "species": "Especie",
            "breed": "Raza",
            "age": "Edad",
            "notes": "Notas",
            "photo": "Foto",
        }


class JobRequestForm(forms.ModelForm):
    class Meta:
        model = JobRequest
        fields = ['pets', 'start_date', 'end_date', 'message']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if owner:
            self.fields['pets'].queryset = Pet.objects.filter(owner=owner)
