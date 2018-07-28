from django.forms import ModelForm
from .models import *

class VoterForm(ModelForm):
    class Meta:
        model = Voter
        exclude = []
