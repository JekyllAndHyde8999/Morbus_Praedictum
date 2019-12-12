# Generated by Django 2.2.7 on 2019-12-12 08:17

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_auto_20191212_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='EyeDonor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name_of_Donor', models.CharField(max_length=50)),
                ('time_f_death', models.TimeField()),
                ('attendee_name', models.CharField(max_length=50)),
                ('contact_info', phonenumber_field.modelfields.PhoneNumberField(max_length=13, region=None)),
                ('City', models.CharField(max_length=50)),
            ],
        ),
    ]
