# Generated by Django 3.1.7 on 2021-04-08 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workout_app', '0038_achievement_has_second_specific_workouttypecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='second_specific_WorkoutTypeCount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sswtc', to='workout_app.workouttypecount'),
        ),
    ]
