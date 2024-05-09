import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    create_date_local = models.DateTimeField(auto_now=True)
    update_date_local = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save()
        if not self.id:
            self.create_date_local = datetime.datetime.now(timezone.timezone.utc).astimezone()
        self.update_date = datetime.datetime.now()
        self.update_date_local = datetime.datetime.now(timezone.timezone.utc).astimezone()

    class Meta:
        abstract = True


# for page CompanyInfo
class CompanyInfo(BaseModel):
    logo = models.CharField(max_length=20)
    history = models.TextField()
    requisites = models.TextField()
    date = models.DateField()


# for page News
class Article(BaseModel):
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    text = models.TextField()
    picture = models.ImageField(upload_to="article_picture", default='')


# for page FAQ
class Faq(BaseModel):
    date = models.DateField()
    question = models.TextField()
    answer = models.TextField()


# for page Vacancies
class Vacancy(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField()
    salary = models.CharField(max_length=40)


# for page Reviews
class Review(BaseModel):
    name = models.TextField()
    grade = models.PositiveSmallIntegerField()
    text = models.TextField()
    date = models.DateTimeField()


# for page Coupons
class Coupon(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField()
    code = models.CharField(max_length=10)
    discount = models.PositiveSmallIntegerField(default=5, validators=[MaxValueValidator(100)])
    end_date = models.DateField()
