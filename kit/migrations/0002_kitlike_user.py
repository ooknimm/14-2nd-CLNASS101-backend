# Generated by Django 3.1.3 on 2021-01-13 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kit', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
