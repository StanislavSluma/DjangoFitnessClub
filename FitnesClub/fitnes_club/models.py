from django.db import models
from django.contrib.auth.models import User
import re
from common_tasks.models import BaseModel
from django.core.validators import ValidationError, MinValueValidator, MaxValueValidator


class Client(BaseModel):
    fullname = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    phone_number = models.CharField(max_length=30)
    expenses = models.FloatField(default=0, validators=[MinValueValidator(0)])
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if not re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', self.phone_number):
            raise ValidationError("Паттерн +375 (ХХ) ХХХ-ХХ-ХХ")


class Group(BaseModel):
    name = models.CharField(max_length=50)
    all_price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    max_workouts = models.PositiveSmallIntegerField(default=10)
    max_clients = models.PositiveSmallIntegerField(default=10)
    is_open = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=True)
    clients = models.ManyToManyField(Client, blank=True)


class Hall(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


class Workout(BaseModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=100, default='Category1')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.group.all_price = self.group.all_price + self.price
        self.group.save()


class Instructor(BaseModel):
    fullname = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    phone_number = models.CharField(max_length=30)
    about = models.TextField(null=True, default=None)
    photo = models.ImageField(upload_to="instructors_photo/", default='')
    workouts = models.ManyToManyField(Workout)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if not re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', self.phone_number):
            raise ValidationError("Номер должен соответствовать паттерну +375 (ХХ) ХХХ-ХХ-ХХ")


class GroupSchedule(BaseModel):
    description = models.TextField()
    group = models.OneToOneField(Group, on_delete=models.CASCADE)


class ClubCard(BaseModel):
    name = models.CharField(max_length=50)
    end_date = models.DateField()
    discount = models.PositiveSmallIntegerField() # 0 < x < 99
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
