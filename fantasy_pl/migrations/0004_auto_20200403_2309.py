# Generated by Django 3.0.4 on 2020-04-03 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy_pl', '0003_auto_20200403_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='news_added',
            field=models.DateTimeField(null=True),
        ),
    ]
