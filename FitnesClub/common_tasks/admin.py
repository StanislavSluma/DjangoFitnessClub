from django.contrib import admin
from .models import *


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
