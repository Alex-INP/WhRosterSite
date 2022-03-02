from django.db import models

from users.models import NormalUser


# Create your models here.
class Weapon(models.Model):
	name = models.CharField("weapon ability name", max_length=250)
	price = models.IntegerField("price", default=0)


class WeaponProfile(models.Model):
	name = models.CharField("weapon ability name", max_length=250, default="single")
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


class Keyword(models.Model):
	name = models.CharField("keyword name", max_length=250)


class FactionKeyword(models.Model):
	name = models.CharField("faction keyword name", max_length=250)


class CodexFaction(models.Model):
	name = models.CharField("codex faction name", max_length=250)


class BattlefieldRole(models.Model):
	name = models.CharField("detachment role name", max_length=250)


class Unit(models.Model):
	name = models.CharField("unit name", max_length=250)
	codex_faction = models.ForeignKey(CodexFaction, on_delete=models.CASCADE, verbose_name="codex faction", related_name="codex_faction")
	detachment_role = models.ForeignKey(BattlefieldRole, on_delete=models.SET_NULL, null=True)
	faction_keywords = models.ManyToManyField(FactionKeyword, verbose_name="faction_keywords", blank=True, related_name="faction_keywords")
	keywords = models.ManyToManyField(Keyword, verbose_name="keywords", blank=True, related_name="keywords")
	wargear_options = models.TextField(verbose_name="wargear options", blank=True)
	abilities = models.ManyToManyField(Ability, verbose_name="abilities", blank=True, related_name="abilities")
	description = models.TextField("description", blank=True)
	power_rating = models.PositiveIntegerField("power rating")
	picture_search_link = models.URLField("picture search link", blank=True)
	weapon = models.ManyToManyField(Weapon, verbose_name="weapon", blank=True, related_name="u_weapon")
	transport = models.TextField("transport", default="")


class UnitModel(models.Model):
	name = models.CharField("unit name", max_length=250)
	price = models.PositiveIntegerField("price")


class UnitModelProfile(models.Model):
	position = models.PositiveIntegerField("position", default=1)
	movement = models.CharField("movement", max_length=100, blank=True)
	weapon_skill = models.PositiveIntegerField("weapon skill", blank=True)
	ballistic_skill = models.PositiveIntegerField("ballistic_skill", blank=True)
	strength = models.CharField("strength", max_length=100, blank=True)
	toughness = models.PositiveIntegerField("toughness", blank=True)
	wounds = models.CharField("wounds", max_length=100, blank=True)
	attacks = models.CharField("attacks", max_length=100, blank=True)
	leadership = models.PositiveIntegerField("leadership", blank=True)
	saving_throw = models.PositiveIntegerField("saving throw", blank=True)
	base = models.CharField("base", blank=True, max_length=50)
	unit_model = models.ForeignKey(UnitModel, on_delete=models.CASCADE, verbose_name="unit", related_name="ump_unit")


class OtherWargear(models.Model):
	name = models.CharField("wargear name", max_length=250)
	description = models.TextField("wargear description")


class OtherWargearInUnits(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="unit", related_name="owiu_unit")
	wargear = models.ForeignKey(OtherWargear, on_delete=models.CASCADE, verbose_name="wargear", related_name="owiu_wargear")
	cost = models.PositiveIntegerField("wargear cost", default=0)


class Roster(models.Model):
	name = models.CharField("unit name", max_length=250)
	user = models.OneToOneField(NormalUser, on_delete=models.CASCADE, verbose_name="user")
	description = models.TextField("description", blank=True)
	total_cost = models.PositiveIntegerField("total roster cost", default=0)
	max_cost = models.PositiveIntegerField("maximum roster cost", default=1500)

	# def get_full_roster_data(self):
	# 	UnitsInRosters.objects.filter(roster=self.pk)


class UnitsInRosters(models.Model):
	roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name="roster")
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="roster_unit")
	unit_model = models.ForeignKey(UnitModel, on_delete=models.CASCADE, related_name="roster_unit_model")
	model_count = models.PositiveIntegerField("model count", default=0)
	# total_cost = models.PositiveIntegerField("total unit cost", default=0)


class WeaponInRosterUnits(models.Model):
	roster_unit = models.ForeignKey(UnitsInRosters, on_delete=models.CASCADE, related_name="roster_unit")
	weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, related_name="roster_unit_weapon")
	count = models.PositiveIntegerField("count", default=0)
	# total_cost = models.PositiveIntegerField("total weapon cost", default=0)


class OtherWargearInRosterUnits(models.Model):
	roster_unit = models.ForeignKey(UnitsInRosters, on_delete=models.CASCADE, related_name="owiru_roster_unit")
	wargear = models.ForeignKey(OtherWargear, on_delete=models.CASCADE, verbose_name="wargear", related_name="owiru_wargear")
	count = models.PositiveIntegerField("count", default=0)
	# total_cost = models.PositiveIntegerField("total weapon cost", default=0)


class UnitsCountRestrictions(models.Model):
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="ucr_unit")
	unit_model = models.ForeignKey(UnitModel, on_delete=models.CASCADE, related_name="unit_model")
	minimum_count = models.PositiveIntegerField("minimum count", default=0)
	maximum_count = models.PositiveIntegerField("maximum count", blank=True)


