from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('namer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='computergroup',
            name='devider',
            field=models.CharField(blank=True, choices=[('', 'None'), (' ', 'Space'), ('-', 'Dash')], default='', max_length=1),
        ),
    ]