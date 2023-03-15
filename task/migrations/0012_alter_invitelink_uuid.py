# Generated by Django 4.1.7 on 2023-03-15 18:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0011_invitelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitelink',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
