from django.db import models


# for page CompanyInfo
class CompanyInfo(models.Model):
    logo = models.CharField(max_length=20)
    history = models.TextField()
    requisites = models.TextField()


# for page News
class Article(models.Model):
    date = models.DateTimeField
    title = models.CharField(max_length=100)
    description = models.TextField()
    text = models.TextField()


# for page FAQ
class Faq(models.Model):
    date = models.DateField()
    question = models.TextField()
    answer = models.TextField()


# for page Contacts
# class Instructor

# for page Vacancies
class Vacancy(models.Model):
    description = models.TextField()
    salary = models.PositiveIntegerField()


# for page Reviews
class Review(models.Model):
    name = models.TextField()
    grade = models.PositiveSmallIntegerField()
    text = models.TextField()
    date = models.DateTimeField()


# for page Coupons
class Coupon(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    code = models.CharField(max_length=10)
    end_date = models.DateField()


