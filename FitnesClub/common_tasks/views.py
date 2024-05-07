import datetime
import calendar
import requests

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Article, CompanyInfo, Coupon, Faq, Vacancy, Employee, Review
from fitnes_club.models import Client
from .forms import ReviewForm


def home_page(request):

    current_datetime = datetime.datetime.now()
    user_timezone = datetime.datetime.now(timezone.timezone.utc).astimezone().tzinfo
    text_calendar = calendar.TextCalendar(firstweekday=2).formatmonth(current_datetime.year, current_datetime.month).split('\n')

    try:
        latest_article = Article.objects.order_by('-date')[0]
    except IndexError:
        latest_article = None
    response = requests.get("https://catfact.ninja/fact")

    if response.status_code == 200:
        cat_api = response.json()
    else:
        cat_api = None
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    if response.status_code == 200:
        dog_api = response.json()
    else:
        dog_api = None

    context = {
        'article': latest_article,
        'cat': cat_api,
        'dog': dog_api,
        'cur_time': current_datetime,
        'calendar': text_calendar,
        'tz': user_timezone
    }
    return render(request, 'HomePage.html', context)


def company_info_page(request):
    info = CompanyInfo.objects.order_by("date")
    return render(request, "CompanyInfoPage.html", {'info': info})


def news_page(request):
    info = Article.objects.order_by("-date")
    return render(request, "NewsPage.html", {'news': info})


def employees_page(request):
    employees = Employee.objects.all()
    return render(request, "EmployeesPage.html", {'employees': employees})


def faq_page(request):
    faqs = Faq.objects.order_by('-date')
    return render(request, "FAQPage.html", {'faqs': faqs})


def vacancies_page(request):
    vac = Vacancy.objects.all()
    return render(request, "VacanciesPage.html", {'vacancies': vac})


def reviews_page(request):
    reviews = Review.objects.order_by('-date')
    return render(request, "ReviewsPage.html", {'reviews': reviews})


def coupons_page(request):
    coupons = Coupon.objects.order_by('-end_date')
    return render(request, "CouponsPage.html", {'coupons': coupons})


def instructors(request, name, age):
    return render(request, "InstructorsPage.html", {'name': name, 'age': age})


def user_is_client(user):
    return user.groups.filter(name='Client').count()


@login_required(login_url='/account/login/')
@user_passes_test(user_is_client, login_url='/account/login/')
def create_review_page(request):
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        name = Client.objects.get(user=request.user).fullname
        date = datetime.datetime.now()
        text = request.POST['text']
        grade = request.POST['grade']
        Review.objects.create(name=name, date=date, text=text, grade=grade)
        return HttpResponseRedirect(reverse('feedback'))
    else:
        return render(request, 'CreateReviewPage.html', {'form': form})


