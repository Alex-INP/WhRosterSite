from django.contrib.auth.forms import forms
from django import forms

from .models import Roster

class NewRosterForm(forms.ModelForm):
	# user = forms.CharField()
	name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	# max_cost = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	max_cost = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
	description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

	class Meta:
		model = Roster
		fields = ("name", "max_cost", "description")

