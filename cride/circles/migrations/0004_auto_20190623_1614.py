# Generated by Django 2.2.2 on 2019-06-23 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0003_auto_20190621_2325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='remaining_invitation',
            new_name='remaining_invitations',
        ),
    ]
