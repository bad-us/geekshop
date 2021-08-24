# Generated by Django 3.1.7 on 2021-04-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_shopuserprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuserprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], db_index=True, max_length=1, verbose_name='пол'),
        ),
    ]
