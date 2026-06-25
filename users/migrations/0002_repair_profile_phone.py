from django.db import migrations


def add_phone_if_missing(apps, schema_editor):
    table_name = 'users_profile'
    with schema_editor.connection.cursor() as cursor:
        columns = [column.name for column in schema_editor.connection.introspection.get_table_description(cursor, table_name)]

    if 'phone' not in columns:
        schema_editor.execute("ALTER TABLE users_profile ADD COLUMN phone varchar(15) NOT NULL DEFAULT ''")


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_phone_if_missing, migrations.RunPython.noop),
    ]
