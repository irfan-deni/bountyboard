from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_claimed_to_in_progress(apps, schema_editor):
    Task = apps.get_model('tasks', 'Task')
    Task.objects.filter(status='claimed').update(status='in_progress')


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_claimed_to_in_progress, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('closed', 'Closed')], default='open', max_length=12),
        ),
        migrations.CreateModel(
            name='Proof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='proofs/')),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hunter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proofs', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hunter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='tasks.task')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('task', 'hunter')},
            },
        ),
    ]
