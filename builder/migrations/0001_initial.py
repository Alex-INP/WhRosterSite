# Generated by Django 4.0.2 on 2022-02-14 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='ability name')),
                ('description', models.TextField(verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='BattlefieldRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='detachment role name')),
            ],
        ),
        migrations.CreateModel(
            name='CodexFaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='codex faction name')),
            ],
        ),
        migrations.CreateModel(
            name='FactionKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='faction keyword name')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='keyword name')),
            ],
        ),
        migrations.CreateModel(
            name='OtherWargear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='wargear name')),
                ('description', models.TextField(verbose_name='wargear description')),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='unit name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('total_cost', models.PositiveIntegerField(default=0, verbose_name='total roster cost')),
                ('max_cost', models.PositiveIntegerField(default=1500, verbose_name='maximum roster cost')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='unit name')),
                ('wargear_options', models.TextField(blank=True, verbose_name='wargear options')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('power_rating', models.PositiveIntegerField(verbose_name='power rating')),
                ('picture_search_link', models.URLField(blank=True, verbose_name='picture search link')),
                ('transport', models.TextField(default='', verbose_name='transport')),
                ('abilities', models.ManyToManyField(blank=True, related_name='abilities', to='builder.Ability', verbose_name='abilities')),
                ('codex_faction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codex_faction', to='builder.codexfaction', verbose_name='codex faction')),
                ('detachment_role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='builder.battlefieldrole')),
                ('faction_keywords', models.ManyToManyField(blank=True, related_name='faction_keywords', to='builder.FactionKeyword', verbose_name='faction_keywords')),
                ('keywords', models.ManyToManyField(blank=True, related_name='keywords', to='builder.Keyword', verbose_name='keywords')),
            ],
        ),
        migrations.CreateModel(
            name='UnitModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='unit name')),
                ('price', models.PositiveIntegerField(verbose_name='price')),
            ],
        ),
        migrations.CreateModel(
            name='UnitsInRosters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_count', models.PositiveIntegerField(default=0, verbose_name='model count')),
                ('roster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster', to='builder.roster')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_unit', to='builder.unit')),
                ('unit_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_unit_model', to='builder.unitmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='weapon ability name')),
                ('price', models.IntegerField(default=0, verbose_name='price')),
            ],
        ),
        migrations.CreateModel(
            name='WeaponProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='single', max_length=250, verbose_name='weapon ability name')),
                ('weapon_range', models.CharField(blank=True, max_length=100, verbose_name='weapon range')),
                ('weapon_type', models.CharField(blank=True, max_length=100, verbose_name='weapon type')),
                ('strength', models.CharField(blank=True, max_length=100, verbose_name='strength')),
                ('armor_penetration', models.CharField(blank=True, max_length=100, verbose_name='armor penetration')),
                ('damage', models.CharField(blank=True, max_length=100, verbose_name='damage')),
                ('abilities', models.TextField(blank=True, verbose_name='abilities')),
                ('weapon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wp_weapon', to='builder.weapon')),
            ],
        ),
        migrations.CreateModel(
            name='WeaponInRosterUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='count')),
                ('roster_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_unit', to='builder.unitsinrosters')),
                ('weapon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_unit_weapon', to='builder.weapon')),
            ],
        ),
        migrations.CreateModel(
            name='UnitsCountRestrictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_count', models.PositiveIntegerField(default=0, verbose_name='minimum count')),
                ('maximum_count', models.PositiveIntegerField(blank=True, verbose_name='maximum count')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ucr_unit', to='builder.unit')),
                ('unit_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_model', to='builder.unitmodel')),
            ],
        ),
        migrations.CreateModel(
            name='UnitModelProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1, verbose_name='position')),
                ('movement', models.PositiveIntegerField(blank=True, verbose_name='movement')),
                ('weapon_skill', models.PositiveIntegerField(blank=True, verbose_name='weapon skill')),
                ('ballistic_skill', models.PositiveIntegerField(blank=True, verbose_name='ballistic_skill')),
                ('strength', models.PositiveIntegerField(blank=True, verbose_name='strength')),
                ('toughness', models.PositiveIntegerField(blank=True, verbose_name='toughness')),
                ('wounds', models.CharField(blank=True, max_length=250, verbose_name='wounds')),
                ('attacks', models.PositiveIntegerField(blank=True, verbose_name='attacks')),
                ('leadership', models.PositiveIntegerField(blank=True, verbose_name='leadership')),
                ('saving_throw', models.PositiveIntegerField(blank=True, verbose_name='saving throw')),
                ('base', models.CharField(blank=True, max_length=50, verbose_name='base')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ump_unit', to='builder.unitmodel', verbose_name='unit')),
            ],
        ),
        migrations.AddField(
            model_name='unit',
            name='weapon',
            field=models.ManyToManyField(blank=True, related_name='u_weapon', to='builder.Weapon', verbose_name='weapon'),
        ),
        migrations.CreateModel(
            name='OtherWargearInUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.PositiveIntegerField(default=0, verbose_name='wargear cost')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owiu_unit', to='builder.unit', verbose_name='unit')),
                ('wargear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owiu_wargear', to='builder.otherwargear', verbose_name='wargear')),
            ],
        ),
        migrations.CreateModel(
            name='OtherWargearInRosterUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='count')),
                ('roster_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owiru_roster_unit', to='builder.unitsinrosters')),
                ('wargear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owiru_wargear', to='builder.otherwargear', verbose_name='wargear')),
            ],
        ),
    ]