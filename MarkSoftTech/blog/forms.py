from django import forms
from .models import Contact, Subscriber



class SubscriberForm(forms.Form):
    email = forms.EmailField(label='Email Address',
                             max_length=100,
                             widget=forms.EmailInput(attrs={'class':'text-input'}))




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'website', 'location', 'subject', 'message']
