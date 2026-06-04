import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transit', '0003_alter_bus_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cooperativa',
                'verbose_name_plural': 'Cooperativas',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='ruta',
            name='cooperativa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rutas', to='transit.cooperativa'),
        ),
    ]
