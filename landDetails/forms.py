from django.forms import ModelForm
from .models import Landmark

class LandForm(ModelForm):
    class Meta:
        model = Landmark
        fields = '__all__'
        exclude = ['host', 'participants']