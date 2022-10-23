from .models import Emotion
from django import forms

class EmotionForm(forms.ModelForm):

    class Meta:
        model = Emotion
        fields = '__all__'
        