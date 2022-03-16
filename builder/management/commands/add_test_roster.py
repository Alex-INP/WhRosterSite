import json

from django.core.management.base import BaseCommand

from builder.models import Roster


class Command(BaseCommand):
	def handle(self, *args, **options):
		roster_units_data = {
			"detachment_data" : [1, 2],
			"main_data": [
				{
					"position_number": 1,
					"unit_pk": 1,
					"models":
						[
							{"model_pk": 1, "model_count": 1}
						],
					"weapons":
						[
							{"weapon_pk": 1, "weapon_count": 1},
							{"weapon_pk": 2, "weapon_count": 1},
							{"weapon_pk": 3, "weapon_count": 1},
							{"weapon_pk": 4, "weapon_count": 1},
						],
					"abilities":
						[
							# {"ability_pk": 1, "bought": True},
							# {"ability_pk": 2, "bought": True},
							# {"ability_pk": 3, "bought": True},
							# {"ability_pk": 4, "bought": True},
							# {"ability_pk": 5, "bought": True},
							# {"ability_pk": 6, "bought": True},
							# {"ability_pk": 7, "bought": True},
						],
					"other_wargear": []
				},
				{
					"position_number": 2,
					"unit_pk": 9,
					"models":
						[
							{"model_pk": 9, "model_count": 6},
							{"model_pk": 10, "model_count": 1}
						],
					"weapons":
						[
							{"weapon_pk": 27, "weapon_count": 1},
							{"weapon_pk": 31, "weapon_count": 6},
						],
					"abilities":
						[
							# {"ability_pk": 1, "bought": True},
							# {"ability_pk": 2, "bought": True},
							# {"ability_pk": 3, "bought": True},
							# {"ability_pk": 4, "bought": True},
							# {"ability_pk": 5, "bought": True},
							# {"ability_pk": 6, "bought": True},
							# {"ability_pk": 7, "bought": True},
						],
					"other_wargear":
						[
							{"wargear_pk": 1, "wargear_count": 1},
							{"wargear_pk": 2, "wargear_count": 1}
						]
				}
			]
		}
		roster = Roster.objects.get(pk=1)
		roster.roster_data = json.dumps(roster_units_data).encode()
		roster.save()
