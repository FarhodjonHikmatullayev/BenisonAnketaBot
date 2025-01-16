# Generated by Django 5.1.4 on 2025-01-16 07:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uzb', models.CharField(max_length=221, verbose_name='Kategoriya nomi(Uzb)')),
                ('title_rus', models.CharField(blank=True, max_length=221, verbose_name='Kategoriya nomi(Rus)')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Vaqt')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Ish kategoriyalari',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uzb', models.CharField(blank=True, max_length=221, null=True, verbose_name='Viloyat nomi(Uzb)')),
                ('name_rus', models.CharField(blank=True, max_length=221, null=True, verbose_name='Viloyat nomi(Rus)')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Vaqt')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Viloyatlar',
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=221, null=True, verbose_name='F.I.Sh')),
                ('username', models.CharField(blank=True, max_length=221, null=True, verbose_name='Username')),
                ('role', models.CharField(blank=True, choices=[('user', 'Oddiy foydalanuvchi'), ('admin', 'Admin')], default='user', max_length=100, null=True, verbose_name='Foydalanuvchi roli')),
                ('telegram_id', models.BigIntegerField(unique=True, verbose_name='Telegram ID')),
                ('language', models.CharField(blank=True, choices=[('rus', 'Rus tili'), ('uzb', "O'zbek tili")], default='uzb', max_length=3, null=True, verbose_name='Til')),
                ('joined_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name="Qo'shilgan vaqti")),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Foydalanuvchilar',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uzb', models.CharField(max_length=221, verbose_name='Filial nomi(Uzb)')),
                ('title_rus', models.CharField(max_length=221, verbose_name='Filial nomi(Rus)')),
                ('description_uzb', models.CharField(max_length=221, verbose_name="Qo'shimcha(Uzb)")),
                ('description_rus', models.CharField(max_length=221, verbose_name="Qo'shimcha(Rus)")),
                ('latitude', models.CharField(max_length=221, verbose_name='Latitude')),
                ('longitude', models.CharField(max_length=221, verbose_name='Longitude')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Vaqt')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.region', verbose_name='Viloyat')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Filiallar',
                'db_table': 'branch',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_uzb', models.CharField(max_length=221, verbose_name='Vakansiya nomi(Uzb)')),
                ('title_rus', models.CharField(max_length=221, verbose_name='Vakansiya nomi(Rus)')),
                ('photo', models.ImageField(upload_to='vacancies/', verbose_name='Rasm')),
                ('description_uzb', models.TextField(verbose_name='Vakansiya haqida(Uzb)')),
                ('description_rus', models.TextField(verbose_name='Vakansiya haqida(Rus)')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Vaqt')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.branch', verbose_name='Filial')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.category', verbose_name='Kategoriya')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anketa.region', verbose_name='Viloyat')),
            ],
            options={
                'verbose_name': 'Vacancy',
                'verbose_name_plural': 'Vakansiyalar',
                'db_table': 'vacancy',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=221, null=True, verbose_name='Ism')),
                ('last_name', models.CharField(blank=True, max_length=221, null=True, verbose_name='Familiya')),
                ('fathers_name', models.CharField(blank=True, max_length=221, null=True, verbose_name='Otasining ismi')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Erkak'), ('female', 'Ayol')], max_length=6, null=True, verbose_name='Jins')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name="Tug'ilgan kun")),
                ('location', models.CharField(blank=True, max_length=221, null=True, verbose_name='Turar joy manzili')),
                ('phone', models.CharField(blank=True, max_length=221, null=True, verbose_name='Telefon')),
                ('email', models.CharField(blank=True, max_length=221, null=True, verbose_name='Elektron pochta')),
                ('username', models.CharField(blank=True, max_length=221, null=True, verbose_name='Telegramdagi username')),
                ('marital_status', models.CharField(blank=True, max_length=221, null=True, verbose_name='Oilaviy ahvoli')),
                ('is_student', models.BooleanField(default=False, verbose_name='Talaba')),
                ('education_form', models.CharField(blank=True, max_length=221, null=True, verbose_name="Ta'lim shakli")),
                ('education_level', models.CharField(blank=True, max_length=221, null=True, verbose_name="Ta'lim darajasi")),
                ('uzb_language_level', models.CharField(blank=True, max_length=221, null=True, verbose_name="O'zbek tili darajasi")),
                ('rus_language_level', models.CharField(blank=True, max_length=221, null=True, verbose_name='Rus tili darajasi')),
                ('computer_level', models.CharField(blank=True, max_length=221, null=True, verbose_name='Kompyuterni bilish darajasi')),
                ('expected_salary', models.CharField(blank=True, max_length=221, null=True, verbose_name='Kutilayotgan ish haqi')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='Surat')),
                ('source_about_vacancy', models.CharField(blank=True, max_length=221, null=True, verbose_name='Vakansiya haqida qayerdan eshitdingiz?')),
                ('agreement', models.CharField(blank=True, max_length=221, null=True, verbose_name='Ommaviy ofera bilan tanishib chiqing')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vaqt')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anketa.branch', verbose_name='Filial')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anketa.category', verbose_name="Ish yo'nalishi")),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anketa.region', verbose_name='Viloyat')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Foydalanuvchi', to='anketa.user')),
                ('vacancy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anketa.vacancy', verbose_name='Vakansiya')),
            ],
            options={
                'verbose_name': 'Resume',
                'verbose_name_plural': 'Rezyumelar',
                'db_table': 'resume',
            },
        ),
    ]
