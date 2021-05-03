# Generated by Django 3.1.7 on 2021-05-03 00:01

import datetime
from django.db import migrations, models
import workout_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_app', '0067_auto_20210502_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutlinked',
            name='end_date',
            field=models.DateField(default=datetime.date.today, validators=[workout_app.models.validate_date_not_future]),
        ),
    ]