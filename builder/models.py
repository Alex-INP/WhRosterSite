import json

from django.db import models

from users.models import NormalUser

# Создать модель для сохранения шаблонов юнитов пользователей

class Detachment(models.Model):
	name = models.CharField("detachment name", max_length=250)
	command_cost = models.CharField("command cost", max_length=50)
	main_restrictions = models.TextField("restrictions")
	command_benefits = models.TextField("command benefits")
	hq_restriction = models.CharField("hq restriction", max_length=50)
	troops_restriction = models.CharField("troops restriction", max_length=50)
	transport_restriction = models.CharField("Dedicated transport restriction", max_length=250)
	elites_restriction = models.CharField("elites restriction", max_length=50)
	fast_attack_restriction = models.CharField("fast attack restriction", max_length=50)
	flyers_restriction = models.CharField("flyers restriction", max_length=50)
	heavy_support_restriction = models.CharField("heavy support restriction", max_length=50)
	lords_of_war_restriction = models.CharField("lords of war restriction", max_length=50)

class Weapon(models.Model):
	name = models.CharField("weapon ability name", max_length=250)
	price = models.CharField("price", max_length=50 ,default="0")

	def get_profiles(self):
		return WeaponProfile.objects.filter(weapon=self)


class WeaponProfile(models.Model):
	name = models.CharField("weapon profile name", max_length=250, default="single")
	weapon_range = models.CharField("weapon range", max_length=100, blank=True)
	weapon_type = models.CharField("weapon type", max_length=100, blank=True)
	strength = models.CharField("strength", max_length=100, blank=True)
	armor_penetration = models.CharField("armor penetration", max_length=100, blank=True)
	damage = models.CharField("damage", max_length=100, blank=True)
	abilities = models.TextField("abilities", blank=True)
	weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, related_name="wp_weapon")


class Ability(models.Model):
	name = models.CharField("ability name", max_length=250)
	description = models.TextField("description")
	price = models.CharField("price", max_length=50, default="0")


class Keyword(models.Model):
	name = models.CharField("keyword name", max_length=250, unique=True)


class FactionKeyword(models.Model):
	name = models.CharField("faction keyword name", max_length=250, unique=True)


class CodexFaction(models.Model):
	name = models.CharField("codex faction name", max_length=250, unique=True)


class BattlefieldRole(models.Model):
	name = models.CharField("detachment role name", max_length=250, unique=True)


class OtherWargear(models.Model):
	name = models.CharField("wargear name", max_length=250, unique=True)
	description = models.TextField("wargear description")
	price = models.PositiveIntegerField("price", default=0)


class Unit(models.Model):
	name = models.CharField("unit name", max_length=250)
	codex_faction = models.ForeignKey(CodexFaction, on_delete=models.CASCADE, verbose_name="codex faction", related_name="codex_faction")
	battlefield_role = models.ForeignKey(BattlefieldRole, on_delete=models.SET_NULL, null=True)
	faction_keywords = models.ManyToManyField(FactionKeyword, verbose_name="faction_keywords", blank=True, related_name="faction_keywords")
	keywords = models.ManyToManyField(Keyword, verbose_name="keywords", blank=True, related_name="keywords")
	wargear_options = models.TextField(verbose_name="wargear options", blank=True, default="")
	abilities = models.ManyToManyField(Ability, verbose_name="abilities", blank=True, related_name="abilities")
	description = models.TextField("description", blank=True)
	power_rating = models.PositiveIntegerField("power rating")
	picture_search_link = models.URLField("picture search link", blank=True, default="")
	weapon = models.ManyToManyField(Weapon, verbose_name="weapon", blank=True, related_name="u_weapon")
	transport = models.TextField("transport", blank=True, default="")
	psyker = models.TextField("psyker", blank=True, default="")
	warlord_trait = models.TextField("warlord trait", blank=True, default="")
	other_wargear = models.ManyToManyField(OtherWargear, verbose_name="other_wargear", related_name="other_wargear")

	def __str__(self):
		return self.name

class UnitModel(models.Model):
	name = models.CharField("unit name", max_length=250)
	price = models.PositiveIntegerField("price")

	def __str__(self):
		return self.name

	def get_profiles(self):
		return sorted(UnitModelProfile.objects.filter(unit_model=self), key=lambda el: el.position)


class UnitModelProfile(models.Model):
	position = models.PositiveIntegerField("position", default=1)
	movement = models.CharField("movement", max_length=100, blank=True)
	weapon_skill = models.PositiveIntegerField("weapon skill", blank=True)
	ballistic_skill = models.CharField("ballistic_skill", max_length=50, blank=True)
	strength = models.CharField("strength", max_length=100, blank=True)
	toughness = models.PositiveIntegerField("toughness", blank=True)
	wounds = models.CharField("wounds", max_length=100, blank=True)
	attacks = models.CharField("attacks", max_length=100, blank=True)
	leadership = models.PositiveIntegerField("leadership", blank=True)
	saving_throw = models.PositiveIntegerField("saving throw", blank=True)
	base = models.CharField("base", blank=True, max_length=50)
	unit_model = models.ForeignKey(UnitModel, on_delete=models.CASCADE, verbose_name="unit", related_name="ump_unit")

class Roster(models.Model):
	name = models.CharField("unit name", max_length=250)
	user = models.ForeignKey(NormalUser, on_delete=models.CASCADE, verbose_name="user")
	description = models.TextField("description", blank=True)
	total_cost = models.PositiveIntegerField("total roster cost", default=0)
	max_cost = models.PositiveIntegerField("maximum roster cost", default=1500)
	factions = models.ManyToManyField(CodexFaction, verbose_name="factions", related_name="factions")
	private = models.BooleanField(default=False)
	roster_data = models.BinaryField(verbose_name="roster data", null=True, default=json.dumps({"detachment_data": [], "main_data": []}).encode())

	def __str__(self):
		return self.name


class UnitsCountRestrictions(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="ucr_unit")
	unit_model = models.ForeignKey(UnitModel, on_delete=models.CASCADE, related_name="unit_model")
	minimum_count = models.PositiveIntegerField("minimum count", default=0)
	maximum_count = models.PositiveIntegerField("maximum count", blank=True)


