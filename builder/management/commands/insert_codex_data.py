import argparse
import json

from django.core.management.base import BaseCommand

from builder.models import Weapon, WeaponProfile, Ability, Keyword, FactionKeyword, Unit, UnitModel, UnitModelProfile, \
	OtherWargear, UnitsCountRestrictions, CodexFaction, BattlefieldRole
from users.models import NormalUser

def fill_simple_table(model, all_data):
	for data in all_data:
		try:
			model.objects.get(name=data["name"])
		except:
			model(**data).save()

def add_simple_ability(all_data):
	for data in all_data:
		try:
			Ability.objects.get(name=data["name"], description=data["description"])
		except:
			Ability(**data).save()

def fill_weapon_profile(all_data):
	for data in all_data:
		data["weapon"] = Weapon.objects.get(name=data["weapon"])
		WeaponProfile(**data).save()

def fill_unit_abilities(unit, abilities):
	for ab in abilities:
		ability_obj = Ability.objects.get(name=ab["name"], description=ab["description"])
		unit.abilities.add(ability_obj)

def fill_unit_dependancy(dependancy_model, dependancy_attribute, all_data):
	for data in all_data:
		dep_obj = dependancy_model.objects.get(name=data)
		dependancy_attribute.add(dep_obj)


def fill_unit(all_data):
	for data in all_data:
		data["codex_faction"] = CodexFaction.objects.get(name=data["codex_faction"])
		data["battlefield_role"] = BattlefieldRole.objects.get(name=data["battlefield_role"])
		if data["wargear_options"]:
			data["wargear_options"] = "\n".join(data["wargear_options"])
		for key, val in data.items():
			if val is None:
				data[key] = ""
		Unit(
			name=data["name"],
			codex_faction=data["codex_faction"],
			battlefield_role=data["battlefield_role"],
			wargear_options=data["wargear_options"],
			description=data["description"],
			power_rating=int(data["power_rating"]),
			picture_search_link=data["picture_search_link"],
			transport=data["transport"],
			psyker=data["psyker"],
			warlord_trait=data["warlord_trait"]
		).save()
		# print(f"{[i.name for i in Unit.objects.filter(name=data['name'])]=}")
		unit = Unit.objects.get(name=data["name"])

		if data["keywords"]:
			fill_unit_dependancy(Keyword, unit.keywords, data["keywords"])
		if data["faction_keywords"]:
			fill_unit_dependancy(FactionKeyword, unit.faction_keywords, data["faction_keywords"])
		if data["weapons"]:
			fill_unit_dependancy(Weapon, unit.weapon, data["weapons"])
		if data["other_wargear"]:
			fill_unit_dependancy(OtherWargear, unit.other_wargear, data["other_wargear"])

		if data["abilities"]:
			fill_unit_abilities(unit, data["abilities"])

def fill_model_n_dependencies(models_data):
	for model in models_data:
		UnitModel(name=model["name"], price=model["price"]).save()
		unit_model = UnitModel.objects.get(name=model["name"])
		unit = Unit.objects.get(name=model["unit_affinity"])
		UnitsCountRestrictions(
			unit=unit,
			unit_model=unit_model,
			minimum_count=model["unit_count_restrictions"]["min"],
			maximum_count=model["unit_count_restrictions"]["max"]
		).save()

def fill_model_profiles(profiles_data):
	for profile in profiles_data:
		profile["unit_model"] = UnitModel.objects.get(name=profile["unit_model"])
		UnitModelProfile(**profile).save()

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument("-f", nargs="?", type=str)

	def handle(self, *args, **options):
		purge_db = False

		file_name = options["f"]
		if file_name is None:
			print("Error: No filename specified. Use -f to specify.")
			return

		with open(f"builder/management/commands/{file_name}", "r", encoding="utf-8") as file:
			file_content = json.load(file)
		if purge_db:
			Keyword.objects.all().delete()
			FactionKeyword.objects.all().delete()
			CodexFaction.objects.all().delete()
			BattlefieldRole.objects.all().delete()
			Weapon.objects.all().delete()
			OtherWargear.objects.all().delete()
			Ability.objects.all().delete()
			WeaponProfile.objects.all().delete()
			Unit.objects.all().delete()
			UnitModel.objects.all().delete()
			UnitModelProfile.objects.all().delete()
		fill_simple_table(Keyword, file_content["keyword_data"])
		fill_simple_table(FactionKeyword, file_content["faction_keyword_data"])
		fill_simple_table(CodexFaction, file_content["codex_faction_data"])
		fill_simple_table(BattlefieldRole, file_content["battlefield_role_data"])
		fill_simple_table(Weapon, file_content["weapon_data"])
		fill_simple_table(OtherWargear, file_content["other_wargear"])
		# fill_simple_table(Ability, file_content["ability_data"])
		add_simple_ability(file_content["ability_data"])

		fill_weapon_profile(file_content["weapon_profile_data"])

		fill_unit(file_content["unit_data"])

		fill_model_n_dependencies(file_content["unit_model_data"])

		fill_model_profiles(file_content["unit_model_profile_data"])

