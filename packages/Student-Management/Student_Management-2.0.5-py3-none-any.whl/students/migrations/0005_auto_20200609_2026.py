from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20200609_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_image_url',
            field=models.CharField(default=3, max_length=9000),
            preserve_default=False,
        ),
    ]
