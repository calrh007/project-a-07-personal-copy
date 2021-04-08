# Generated by Django 3.1.7 on 2021-04-08 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout_app', '0036_auto_20210407_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='has_second_specific_workoutType',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='achievement',
            name='second_specific_workoutType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sswt', to='workout_app.workouttype'),
        ),
    ]