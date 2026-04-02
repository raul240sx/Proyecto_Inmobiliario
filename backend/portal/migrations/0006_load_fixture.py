from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    """Carga automáticamente el fixture con datos de regiones y comunas"""
    call_command('loaddata', 'respaldo_portal_users')


def unload_fixture(apps, schema_editor):
    """No hace nada si se revierte - los datos permanecen"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_solicituddocumento'),
    ]

    operations = [
        migrations.RunPython(load_fixture, unload_fixture),
    ]
