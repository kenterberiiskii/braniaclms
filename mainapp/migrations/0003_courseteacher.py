# Generated by Django 4.1.2 on 2022-10-27 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_course_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=256, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=256, verbose_name='Фамилия')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Создан')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('courses', models.ManyToManyField(to='mainapp.course')),
            ],
            options={
                'verbose_name': 'курс к учителю',
                'verbose_name_plural': 'курсы к учителям',
            },
        ),
    ]
