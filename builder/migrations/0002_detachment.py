# Generated by Django 4.0.2 on 2022-03-16 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='detachment name')),
                ('command_cost', models.CharField(max_length=50, verbose_name='command cost')),
                ('main_restrictions', models.TextField(verbose_name='restrictions')),
                ('command_benefits', models.TextField(verbose_name='command benefits')),
                ('hq_restriction', models.CharField(max_length=50, verbose_name='hq restriction')),
                ('troops_restriction', models.CharField(max_length=50, verbose_name='troops restriction')),
                ('transport_restriction', models.CharField(max_length=250, verbose_name='Dedicated transport restriction')),
                ('elites_restriction', models.CharField(max_length=50, verbose_name='elites restriction')),
                ('fast_attack_restriction', models.CharField(max_length=50, verbose_name='fast attack restriction')),
                ('flyers_restriction', models.CharField(max_length=50, verbose_name='flyers restriction')),
                ('heavy_support_restriction', models.CharField(max_length=50, verbose_name='heavy support restriction')),
                ('lords_of_war_restriction', models.CharField(max_length=50, verbose_name='lords of war restriction')),
            ],
        ),
    ]
