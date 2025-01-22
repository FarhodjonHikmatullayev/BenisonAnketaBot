from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'role', 'username', 'language', 'telegram_id', 'joined_at')
    search_fields = ('username', 'language', 'telegram_id')
    list_filter = ('joined_at', 'language', 'role')
    date_hierarchy = 'joined_at'


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uzb', 'created_at')
    search_fields = ('name_uzb',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Category)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_uzb', 'created_at')
    search_fields = ('title_uzb',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_uzb', 'region', 'created_at')
    search_fields = ('title_uzb', 'region__name_uzb')
    list_filter = ('created_at', 'region__name_uzb')
    date_hierarchy = 'created_at'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_uzb', 'branch', 'created_at')
    search_fields = ('title_uzb', 'branch__title_uzb')
    list_filter = ('created_at', 'branch__title_uzb', 'region__name_uzb')
    date_hierarchy = 'created_at'


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'vacancy', 'gender', 'date_of_birth', 'location', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'username', 'phone', 'vacancy__title_uzb')
    list_filter = (
        'branch__title_uzb', 'region__name_uzb', 'vacancy__title_uzb',
        'gender', 'is_student', 'created_at', 'category', 'marital_status', 'education_form', 'education_level',
        'uzb_language_level', 'rus_language_level', 'computer_level', 'source_about_vacancy')
    date_hierarchy = 'created_at'
