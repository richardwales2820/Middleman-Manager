# Generated by Django 2.0.1 on 2018-02-01 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mm_manager', '0002_auto_20180131_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='person_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mm_manager.GarlicUser'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='person_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='mm_manager.GarlicUser'),
        ),
    ]
