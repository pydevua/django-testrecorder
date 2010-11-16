from django import forms
from main.models import News

class NewsForm(forms.ModelForm):
    
    class Meta:
        model = News