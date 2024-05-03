from django.db import models
from django.contrib.auth.models import User
import re
from django.core.validators import ValidationError


class Client(models.Model):
    fullname = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    phone_number = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if not re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', self.phone_number):
            raise ValidationError("This field accepts mail id of google only")


class Group(models.Model):
    name = models.CharField(max_length=50)
    all_price = models.PositiveIntegerField()
    clients = models.ManyToManyField(Client)


class Hall(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


class Workout(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    halls = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True)


class Instructor(models.Model):
    fullname = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    phone_number = models.CharField(max_length=30)
    workouts = models.ManyToManyField(Workout)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if not re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', self.phone_number):
            raise ValidationError("Номер долже нсоответствовать паттерну +375 (ХХ) ХХХ-ХХ-ХХ")


class GroupSchedule(models.Model):
    description = models.TextField()
    group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)


class InstructorSchedule(models.Model):
    description = models.TextField()
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE, primary_key=True)


class ClubCard(models.Model):
    name = models.CharField(max_length=50)
    end_date = models.DateField()
    discount = models.PositiveSmallIntegerField() # 0 < x < 99
    client = models.OneToOneField(Client, on_delete=models.CASCADE, primary_key=True)
