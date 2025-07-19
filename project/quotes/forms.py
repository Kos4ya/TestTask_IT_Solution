from django import forms
from .models import Quote, Source, SourceType


class SourceTypeForm(forms.ModelForm):
    class Meta:
        model = SourceType
        fields = ['name']


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'type']
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'})
        }


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': 1})
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError("Такая цитата уже существует")
        return text
