from django.contrib import admin
from .models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')


@admin.register(GroupSchedule)
class GroupScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')


@admin.register(ClubCard)
class ClubCardAdmin(admin.ModelAdmin):
    list_display = ('client', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
    list_filter = ('create_date', 'update_date')
