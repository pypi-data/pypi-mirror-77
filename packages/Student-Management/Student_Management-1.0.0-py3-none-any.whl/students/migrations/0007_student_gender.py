from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20200610_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.TextField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default='', null=True),
        ),
    ]
