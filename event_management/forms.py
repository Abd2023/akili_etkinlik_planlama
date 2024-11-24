from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'category', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'placeholder': 'HH:MM'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'placeholder': 'HH:MM'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%Y-%m-%d']
