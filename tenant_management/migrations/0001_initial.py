# Generated by Django 5.0 on 2023-12-31 06:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Tenants',
            },
        ),
        migrations.CreateModel(
            name='TenantAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement_end_date', models.DateField()),
                ('monthly_rent_date', models.IntegerField()),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant_management.tenant')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_management.unit')),
            ],
        ),
    ]
