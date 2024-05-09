from django.contrib import admin
from .models import *


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(GroupSchedule)
class GroupScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(ClubCard)
class ClubCardAdmin(admin.ModelAdmin):
    list_display = ('client', 'create_date', 'update_date', 'create_date_local', 'update_date_local')


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_date', 'update_date', 'create_date_local', 'update_date_local')
