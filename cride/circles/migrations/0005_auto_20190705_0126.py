# Generated by Django 2.2.3 on 2019-07-05 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0004_auto_20190623_1614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='used_invitation',
            new_name='used_invitations',
        ),
    ]