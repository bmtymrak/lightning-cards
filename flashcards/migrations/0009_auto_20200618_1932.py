# Generated by Django 3.0.6 on 2020-06-18 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0008_auto_20200529_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-front']},
        ),
        migrations.AddField(
            model_name='card',
            name='proficiency',
            field=models.IntegerField(default=0),
        ),
    ]
