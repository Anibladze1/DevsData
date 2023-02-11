from django.forms import ModelForm
from .models import Event, Reservation


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email']