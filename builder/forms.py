from django import forms

from .models import Roster, CodexFaction

class NewRosterForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	max_cost = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
	description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	factions = forms.MultipleChoiceField(choices=[[faction.pk, faction.name] for faction in CodexFaction.objects.all()])

	class Meta:
		model = Roster
		fields = ("name", "max_cost", "description", "factions")


