# Generated by Django 5.0.6 on 2024-07-09 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='avatar.jpg', upload_to='static/profile_pictures/'),
        ),
    ]
