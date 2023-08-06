from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('presence', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=500)),
                ('course_fee', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fees_paid', models.FloatField()),
                ('status', models.CharField(choices=[('ENR', 'Enrolled'), ('IPR', 'In-progress'), ('DSC', 'Discontinued'), ('CMP', 'Completed')], default='ENR', max_length=3)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.course')),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inst_student_id', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('dob1', models.DateField()),
                ('parent_name1', models.CharField(max_length=80)),
                ('parent_name2', models.CharField(max_length=80)),
                ('contact_number1', models.CharField(max_length=14)),
                ('contact_number2', models.CharField(max_length=14)),
                ('joining_date', models.DateField()),
                ('email_id', models.CharField(max_length=360)),
                ('student_image_url', models.CharField(max_length=9000)),
            ],
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.course'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student'),
        ),
    ]
