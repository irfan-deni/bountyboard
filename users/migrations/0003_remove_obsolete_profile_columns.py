from django.db import migrations


def remove_obsolete_profile_columns(apps, schema_editor):
    table_name = 'users_profile'
    obsolete_columns = ['role', 'rank', 'xp', 'rating', 'bio', 'avatar']

    with schema_editor.connection.cursor() as cursor:
        columns = [column.name for column in schema_editor.connection.introspection.get_table_description(cursor, table_name)]

    for column in obsolete_columns:
        if column in columns:
            schema_editor.execute(f'ALTER TABLE {table_name} DROP COLUMN {column}')


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_repair_profile_phone'),
    ]

    operations = [
        migrations.RunPython(remove_obsolete_profile_columns, migrations.RunPython.noop),
    ]
