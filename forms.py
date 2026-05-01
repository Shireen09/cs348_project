from django import forms
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from .models import Country


class CountryForm(forms.ModelForm):
    population = forms.IntegerField(min_value=0, validators=[MinValueValidator(0)])

    class Meta:
        model = Country
        fields = '__all__'

    def clean_code(self):
        code = self.cleaned_data["code"].strip().upper()
        if not code.isalnum():
            raise forms.ValidationError("Country code must be alphanumeric.")
        return code

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not slugify(name):
            raise forms.ValidationError("Country name must contain letters or numbers.")
        return name