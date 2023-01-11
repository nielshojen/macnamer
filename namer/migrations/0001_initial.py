from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('prefix', models.CharField(blank=True, max_length=200, null=True, verbose_name='Computer Name Prefix')),
                ('devider', models.CharField(blank=True, choices=[('', 'None'), (' ', 'Space'), ('-', 'Dash')], default='', max_length=1)),
                ('domain', models.CharField(blank=True, max_length=200, null=True, verbose_name='Computer Domain')),
                ('key', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('network', models.CharField(max_length=200, unique=True)),
                ('computergroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='namer.computergroup')),
            ],
            options={
                'ordering': ['network'],
            },
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Computer Name')),
                ('serial', models.CharField(max_length=200, unique=True, verbose_name='Serial Number')),
                ('last_checkin', models.DateTimeField(blank=True, null=True)),
                ('computergroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='namer.computergroup')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
