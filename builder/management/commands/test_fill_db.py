import json

from django.core.management.base import BaseCommand

import builder.models as builder_models
from users.models import NormalUser


def insert_unit_relations_to_db(unit_instance, keyw, faction_keyw, abilities, weapons):
	for i in keyw:
		object = builder_models.Keyword.objects.get(name=i)
		unit_instance.keywords.add(object)

	for i in faction_keyw:
		object = builder_models.FactionKeyword.objects.get(name=i)
		unit_instance.faction_keywords.add(object)

	for i in abilities:
		object = builder_models.Ability.objects.get(name=i)
		unit_instance.abilities.add(object)

	for i in weapons:
		object = builder_models.Weapon.objects.get(name=i)
		unit_instance.weapon.add(object)

def insert_units_count_restrictions_relations_to_db(unit_instance, unit_models, restrictions):
	last_id = builder_models.UnitsCountRestrictions.objects.latest("id").id
	for index, val in enumerate(unit_models):
		last_id += 1
		unit_model = builder_models.UnitModel.objects.get(name=val)
		builder_models.UnitsCountRestrictions(last_id, unit_instance, unit_model, restrictions[index][0], restrictions[index][1])


class Command(BaseCommand):
	def handle(self, *args, **options):
		with open("builder/management/commands/test_data.json", "r", encoding="utf-8") as file:
			file_content = json.load(file)

		NormalUser.objects.all().delete()
		builder_models.BattlefieldRole.objects.all().delete()
		builder_models.CodexFaction.objects.all().delete()
		builder_models.Weapon.objects.all().delete()
		builder_models.WeaponProfile.objects.all().delete()
		builder_models.Ability.objects.all().delete()
		builder_models.Keyword.objects.all().delete()
		builder_models.FactionKeyword.objects.all().delete()
		builder_models.Unit.objects.all().delete()
		builder_models.UnitModel.objects.all().delete()
		builder_models.UnitModelProfile.objects.all().delete()
		builder_models.Roster.objects.all().delete()
		builder_models.UnitsInRosters.objects.all().delete()
		builder_models.UnitsCountRestrictions.objects.all().delete()


		NormalUser.objects.create_superuser("Admin", "admin@mail.ru", "admin")
		user_one = NormalUser(**{"username": "Alex", "email": "asdasd@mail.ru"})
		user_one.set_password("Q1wertyu")
		user_one.save()

		for codex_faction in file_content["codex_faction_data"]:
			builder_models.CodexFaction(**codex_faction).save()

		for battle_role in file_content["battlefield_role_data"]:
			builder_models.BattlefieldRole(**battle_role).save()

		for weap in file_content["weapon_data"]:
			builder_models.Weapon(**weap).save()

		for weap_profile in file_content["weapon_profile_data"]:
			weap_profile["weapon"] = builder_models.Weapon.objects.get(pk=weap_profile["weapon"])
			builder_models.WeaponProfile(**weap_profile).save()

		for ability in file_content["ability_data"]:
			builder_models.Ability(**ability).save()

		for keyword in file_content["keyword_data"]:
			builder_models.Keyword(**keyword).save()

		for fac_keyword in file_content["faction_keyword_data"]:
			builder_models.FactionKeyword(**fac_keyword).save()

		for unit in file_content["unit_data"]:
			unit["codex_faction"] = builder_models.CodexFaction.objects.get(pk=unit["codex_faction"])
			builder_models.Unit(**unit).save()

		for unit_model in file_content["unit_model_data"]:
			builder_models.UnitModel(**unit_model).save()

		for unit_model_profile in file_content["unit_model_profile_data"]:
			unit_model_profile["unit_model"] = builder_models.UnitModel.objects.get(pk=unit_model_profile["unit_model"])
			builder_models.UnitModelProfile(**unit_model_profile).save()

		for roster in file_content["roster_data"]:
			# user = NormalUser.objects.get(pk=roster["user"])
			user = NormalUser.objects.get(pk=user_one.pk)
			builder_models.Roster(roster["id"], roster["name"], user.pk, roster["description"]).save()

		for unit_count in file_content["unit_count_restriction_data"]:
			unit_count["unit"] = builder_models.Unit.objects.get(pk=unit_count["unit"])
			unit_count["unit_model"] = builder_models.UnitModel.objects.get(pk=unit_count["unit_model"])
			builder_models.UnitsCountRestrictions(**unit_count).save()

		unit_1 = builder_models.Unit.objects.get(pk=1)
		unit_1_keyw = ["BIKER", "KATAPHRON SERVITORS", "KATAPHRON DESTROYERS"]
		unit_1_faction_keyw = ["IMPERIUM", "ADEPTUS MECHANICUS", "CULT MECHANICUS", "<FORGE WORLD>"]
		unit_1_abilities = ["Canticles of the Omnissiah", "Tracked Mobility", "Bionics"]
		unit_1_weapons = ["Cognis flamer (Kataphron Destroyers)", "Heavy grav-cannon", "Kataphron plasma culverin (Kataphron Destroyers)", "Phosphor blaster"]
		unit_1_unit_models = ["Kataphron Destroyer"]
		unit_2 = builder_models.Unit.objects.get(pk=2)
		unit_2_keyw = ["VEHICLE", "TRANSPORT", "DATA-TETHER", "SKORPIUS ENGINE", "SKORPIUS DUNERIDER"]
		unit_2_faction_keyw = ["IMPERIUM", "ADEPTUS MECHANICUS", "SKITARII", "<FORGE WORLD>"]
		unit_2_abilities = ["Doctrina Imperatives", "Explodes", "Broad Spectrum Data-tether"]
		unit_2_weapons = ["Cognis heavy stubber", "Twin cognis heavy stubber"]
		unit_2_unit_models = ["Skorpius Dunerider"]

		insert_unit_relations_to_db(unit_1, unit_1_keyw, unit_1_faction_keyw, unit_1_abilities, unit_1_weapons)
		insert_unit_relations_to_db(unit_2, unit_2_keyw, unit_2_faction_keyw, unit_2_abilities, unit_2_weapons)
		insert_units_count_restrictions_relations_to_db(unit_1, unit_1_unit_models, [[3, 6]])
		insert_units_count_restrictions_relations_to_db(unit_2, unit_2_unit_models, [[1, 1]])

		roster = builder_models.Roster.objects.get(pk=1)

		unit_model_1 = builder_models.UnitsCountRestrictions.objects.get(unit=unit_1.pk).unit_model
		unit_model_2 = builder_models.UnitsCountRestrictions.objects.get(unit=unit_2.pk).unit_model

		roster_unit_1_1 = builder_models.UnitsInRosters(1, roster.pk, unit_1.pk, unit_model_1.pk, 3).save()
		roster_unit_1_2 = builder_models.UnitsInRosters(2, roster.pk, unit_1.pk, unit_model_1.pk, 4).save()
		roster_unit_2_1 = builder_models.UnitsInRosters(3, roster.pk, unit_2.pk, unit_model_2.pk, 1).save()

		builder_models.WeaponInRosterUnits(1, roster_unit_1_1, builder_models.Weapon.objects.get(pk=1), 3)
		builder_models.WeaponInRosterUnits(2, roster_unit_1_1, builder_models.Weapon.objects.get(pk=2), 3)
		builder_models.WeaponInRosterUnits(3, roster_unit_1_2, builder_models.Weapon.objects.get(pk=2), 4)
		builder_models.WeaponInRosterUnits(4, roster_unit_2_1, builder_models.Weapon.objects.get(pk=5), 1)



		# for i in weapon_profile_objects:
			# print(i.pk)
			# print(i.name)
			# print(i.weapon_type)
			# print(i.strength)
			# print(i.armor_penetration)
			# print(i.damage)
			# print(i.abilities)
			# print(i.weapon.name)

		# for i in builder_models.WeaponProfile.objects.all():
		# 	print(i.name)
		# 	print(i.weapon.price)




