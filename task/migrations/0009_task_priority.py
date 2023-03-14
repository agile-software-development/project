# Generated by Django 4.1.7 on 2023-03-14 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_workspace_board_workspace'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2),
        ),
    ]
