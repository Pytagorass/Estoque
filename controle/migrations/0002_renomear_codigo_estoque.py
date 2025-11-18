from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("controle", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="sku",
            new_name="codigo_estoque",
        ),
    ]
