from django import forms
from .models import UploadImage
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['image']