import json
from itertools import chain

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.http import JsonResponse
from django.db.models import Q
from django.db import connection

from .models import Roster, Unit, UnitModel, UnitsCountRestrictions, CodexFaction, Ability, OtherWargear, Weapon, \
    UnitModelProfile, WeaponProfile, Detachment
from .forms import NewRosterForm
from users.models import NormalUser


def get_all_units_data(faction_id):
    all_units = Unit.objects.filter(codex_faction=faction_id)
    final_data = []
    for unit in all_units:
        result = {
            "unit": unit,
            "models": None,
            "weapons": None,
            "abilities": None,
            "other_wargear": None,
        }

        restrictions = UnitsCountRestrictions.objects.select_related("unit").select_related("unit_model").filter(
            unit=unit.pk)
        all_models = []
        for restr in restrictions:
            all_models.append(
                {
                    "model": restr.unit_model,
                    "profiles": sorted(UnitModelProfile.objects.filter(unit_model=restr.unit_model),
                                       key=lambda el: el.position),
                    "count": 0,
                    "count_restrictions": {"min": restr.minimum_count, "max": restr.maximum_count}
                }
            )
        result["models"] = all_models

        all_weapons = []
        weapons = Weapon.objects.filter(u_weapon=unit)
        for weapon in weapons:
                all_weapons.append(
                    {
                        "weapon": weapon,
                        "profiles": WeaponProfile.objects.filter(weapon=weapon),
                        "count": 0,
                    }
                )
        result["weapons"] = all_weapons

        all_abilities = []
        abilities = unit.abilities.all()
        for ability in abilities:
            all_abilities.append(
                {
                    "ability": ability,
                    "bought": True
                }
            )
        result["abilities"] = all_abilities

        all_wargear = []
        wargear = unit.other_wargear.all()
        for wgr in wargear:
            all_wargear.append(
                {
                    "wargear": wgr,
                    "count": 0
                }
            )
        result["other_wargear"] = all_wargear

        final_data.append(result)
    return final_data


def unpack_roster_data(roster):
    return json.loads(roster.roster_data.decode())

def extract_models(unit_dict):
    all_models = []
    restrictions = UnitsCountRestrictions.objects.select_related("unit").select_related("unit_model").filter(
        unit=unit_dict["unit_pk"])

    for restr in restrictions:
        for model in unit_dict["models"]:
            if model["model_pk"] == restr.unit_model.pk:
                all_models.append(
                    {
                        "model": restr.unit_model,
                        "profiles": sorted(UnitModelProfile.objects.filter(unit_model=restr.unit_model), key=lambda el: el.position),
                        "count": model["model_count"],
                        "count_restrictions": {"min": restr.minimum_count, "max": restr.maximum_count}
                    }
                )
    return all_models

def extract_weapons(unit_dict, unit_obj):
    all_weapons = []
    weapons = Weapon.objects.filter(u_weapon=unit_obj) #unit_obj.u_weapon.all()

    # ПРОТЕСТИРОВАТЬ СОКРАЩЕНИЕ КОЛ-ВА ЗАПРОСОВ
    # weapons = Weapon.objects.prefetch_related("wp_weapon").filter(u_weapon=unit_obj)

    for weapon in weapons:
        for w_entry in unit_dict["weapons"]:
            if w_entry["weapon_pk"] == weapon.pk:
                all_weapons.append(
                    {
                        "weapon": weapon,
                        "profiles": WeaponProfile.objects.filter(weapon=weapon),
                        "count": w_entry["weapon_count"],
                    }
                )
    return all_weapons

def extract_abilities(unit_dict, unit_obj):
    all_abilities = []
    abilities = unit_obj.abilities.all()
    for ability in abilities:
        for a_entry in unit_dict["abilities"]:
            if a_entry["ability_pk"] == ability.pk:
                all_abilities.append(
                    {
                        "ability": ability,
                        "bought": a_entry["bought"]
                    }
                )
    return all_abilities

def extract_other_wargear(unit_dict, unit_obj):
    all_wargear = []
    wargear = unit_obj.other_wargear.all()
    for wgr in wargear:
        for w_entry in unit_dict["other_wargear"]:
            if w_entry["wargear_pk"] == wgr.pk:
                all_wargear.append(
                    {
                        "wargear": wgr,
                        "count": w_entry["wargear_count"]
                    }
                )
    return all_wargear

def get_roster_context(roster):
    data = unpack_roster_data(roster)
    final_data = {
            "detachment_data": [Detachment.objects.get(pk=det_pk) for det_pk in data["detachment_data"]],
            "main_data": []
        }

    for unit in data["main_data"]:
        result = {
            "position_number": unit["position_number"],
            "unit": None,
            "models": None,
            "weapons": None,
            "abilities": None,
            "other_wargear": None,
        }

        unit_obj = Unit.objects \
            .select_related("codex_faction") \
            .get(pk=unit["unit_pk"])

        result["unit"] = unit_obj
        result["models"] = extract_models(unit)
        result["weapons"] = extract_weapons(unit, unit_obj)
        result["abilities"] = extract_abilities(unit, unit_obj)
        result["other_wargear"] = extract_other_wargear(unit, unit_obj)

        final_data["main_data"].append(result)
    from pprint import pprint
    # pprint(final_data, sort_dicts=False)

    return final_data



# Create your views here.

class FactionUnitsListView(ListView):
    template_name = "builder/units_list.html"

    def get(self, request, *args, **kwargs):
        all_factions = CodexFaction.objects.all()
        all_units = {}
        if kwargs:
            if faction_pk := kwargs["pk"]:
                all_units = {
                    "HQ": [],
                    "Troops": [],
                    "Dedicated_Transport": [],
                    "Elites": [],
                    "Fast_Attack": [],
                    "Flyers": [],
                    "Heavy_Support": [],
                    "Lords_of_War": []
                }
                faction = CodexFaction.objects.get(id=faction_pk)
                units = Unit.objects.filter(codex_faction=faction)
                for unit in units:
                    all_units[unit.battlefield_role.name.replace(" ", "_")].append(
                        {
                            "unit": unit,
                            "model_restrictions": UnitsCountRestrictions.objects.filter(unit=unit)
                        }
                    )

        return render(
            request, self.template_name, {
                "all_units": all_units, "factions": all_factions})

class WorkboardView(UpdateView):
    template_name = "builder/workboard.html"
    model = Roster

    def get(self, request, *args, **kwargs):
        # if roster_pk := kwargs["pk"]:
        #     self.object = Roster.objects.get(pk=roster_pk)
        return render(request, self.template_name)



# class BuilderListView(ListView):
#     template_name = "builder/workboard.html"
#
#     def get_queryset(self):
#         roster = Roster.objects.get(pk=1)
#         unit_entries = UnitsInRosters.objects.filter(
#             roster=roster).select_related("unit")
#
#         count_restrictions = {}
#         return {
#             "roster": roster,
#             "unit_entries": unit_entries,
#             "count_restrictions": count_restrictions}


class RosterListView(ListView):
    template_name = "builder/roster_list.html"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {
                "rosters": Roster.objects.prefetch_related("factions").filter(user=request.user.pk),
            }
        )


class DisplayRosterListView(ListView):
    template_name = "builder/display_roster.html"

    def get(self, request, *args, **kwargs):
        roster = Roster.objects.get(pk=kwargs["pk"])
        context = get_roster_context(roster)
        return render(
            request,
            self.template_name,
            {
                "roster": roster,
                "detachments": context["detachment_data"],
                "units_list": sorted(context["main_data"], key=lambda x: x["position_number"])
            }
        )

class ManageRosterListView(ListView):
    template_name = "builder/manage_roster.html"

    def get(self, request, *args, **kwargs):
        roster = Roster.objects.get(pk=kwargs["pk"])
        context = get_roster_context(roster)
        return render(
            request,
            self.template_name,
            {
                "all_faction_units": get_all_units_data(1), #Unit.objects.filter(codex_faction=1),
                "roster": roster,
                "detachments": context["detachment_data"],
                "units_list": sorted(context["main_data"], key=lambda x: x["position_number"]),
                "all_detachments": Detachment.objects.all(),
                'data': json.dumps({"data_1": 33, "data_2": "mydata"})
            }
        )

class ManageRosterAJAXView(View):
    def get(self, request, *args, **kwargs):
        faction_units = Unit.objects.filter(faction=kwargs["pk"])
        return JsonResponse({"1": 1})


class CreateRosterView(CreateView):
    template_name = "builder/roster_create.html"
    model = Roster
    form_class = NewRosterForm
    success_url = "builder:roster_list"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = NormalUser.objects.get(pk=request.user.pk)
            form_obj.save()
        return HttpResponseRedirect(reverse_lazy(self.success_url))

