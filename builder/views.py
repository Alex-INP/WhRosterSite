from itertools import chain

from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Roster, Unit, UnitsInRosters, UnitModel
# Create your views here.

class BuilderListView(ListView):
	template_name = "builder/workboard.html"
	# model = Roster

	# def get(self, request, *args, **kwargs):
	# 	self.object = Roster.objects.get(pk=1)
	# 	return render(request, self.template_name)

	def get_queryset(self):
		roster = Roster.objects.get(pk=1)
		units = UnitsInRosters.objects.filter(roster=roster)
		# unit_models = UnitModel.miu_unit.all() filter(pk=ModelsInUnits.objects.)
		return {"roster": roster, "units": units}
		# units_in_roster = Unit.object.filter(pk=)


