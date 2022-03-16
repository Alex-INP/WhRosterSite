import json

from django.core.management.base import BaseCommand

from builder.models import Detachment

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument("-f", nargs="?", type=str)

	def handle(self, *args, **options):
		with open(f"builder/management/commands/data_detachments.json", "r", encoding="utf-8") as file:
			file_content = json.load(file)

		Detachment.objects.all().delete()
		for detach in file_content:
			Detachment(**detach).save()