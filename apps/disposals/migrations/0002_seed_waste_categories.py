from django.db import migrations


CATEGORIES = ["Computadores", "Smartphones", "Tablets", "Fones", "Carregadores", "Outros"]


def seed_categories(apps, schema_editor):
    WasteCategory = apps.get_model("disposals", "WasteCategory")
    for name in CATEGORIES:
        WasteCategory.objects.get_or_create(name=name)


def remove_categories(apps, schema_editor):
    WasteCategory = apps.get_model("disposals", "WasteCategory")
    WasteCategory.objects.filter(name__in=CATEGORIES).delete()


class Migration(migrations.Migration):
    dependencies = [("disposals", "0001_initial")]
    operations = [migrations.RunPython(seed_categories, remove_categories)]
