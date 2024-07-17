# Generated by Django 5.0.6 on 2024-07-17 17:53

import django.db.models.deletion
import django.utils.timezone
import main.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(default='static/profile_pictures/9334228.jpg', upload_to='static/profile_pictures/')),
                ('user_type', models.CharField(choices=[('client', 'Client'), ('freelancer', 'Freelancer')], default='client', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_status', models.CharField(blank=True, max_length=50, null=True)),
                ('payer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('step1_status', models.CharField(choices=[('D', 'Delivered'), ('I', 'In Progress'), ('P', 'Pending')], default='P', max_length=1)),
                ('step1_file', models.FileField(blank=True, null=True, upload_to='static/project_files/step1')),
                ('step2_status', models.CharField(choices=[('D', 'Delivered'), ('I', 'In Progress'), ('P', 'Pending')], default='P', max_length=1)),
                ('step2_file', models.FileField(blank=True, null=True, upload_to='static/project_files/step2')),
                ('step3_status', models.CharField(choices=[('D', 'Delivered'), ('I', 'In Progress'), ('P', 'Pending')], default='P', max_length=1)),
                ('step3_file', models.FileField(blank=True, null=True, upload_to='static/project_files/step3')),
                ('step4_status', models.CharField(choices=[('D', 'Delivered'), ('I', 'In Progress'), ('P', 'Pending')], default='P', max_length=1)),
                ('step4_file', models.FileField(blank=True, null=True, upload_to='static/project_files/step4')),
                ('step5_status', models.CharField(choices=[('D', 'Delivered'), ('I', 'In Progress'), ('P', 'Pending')], default='P', max_length=1)),
                ('step5_file', models.FileField(blank=True, null=True, upload_to='static/project_files/step5')),
                ('client', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'client'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_projects', to='main.profile')),
                ('freelancer', models.ForeignKey(blank=True, limit_choices_to={'user_type': 'freelancer'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='freelancer_projects', to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='static/order_message_files/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to='main.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to='main.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Service Title', max_length=200)),
                ('description', models.TextField()),
                ('features', models.JSONField(default=list, help_text='List of features')),
                ('detailed_description', models.TextField(default='')),
                ('price_essential', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('price_essential_description', models.CharField(default='Essential plan description', max_length=200)),
                ('duration_days', models.IntegerField(default=1, help_text='Duration of the service in days')),
                ('photo', models.ImageField(blank=True, help_text='Service photo', null=True, upload_to='static/service/')),
                ('categorie', models.ForeignKey(default=main.models.Categorie.get_default_category, on_delete=django.db.models.deletion.CASCADE, to='main.categorie')),
                ('freelancer', models.ForeignKey(limit_choices_to={'user_type': 'freelancer'}, on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.service'),
        ),
    ]
