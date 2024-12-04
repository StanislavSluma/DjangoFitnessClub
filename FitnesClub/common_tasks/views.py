import datetime
import calendar
from functools import reduce

import requests

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView

from .models import Article, CompanyInfo, Coupon, Faq, Vacancy, Review
from fitnes_club.models import Client, Instructor, Partner
from .forms import ReviewForm

from django.core.paginator import Paginator
from django.shortcuts import render

def polygon1_page(request):
    return render(request, "Polygon1.html")


def polygon2_page(request):
    return render(request, "Polygon2.html")


def home_page(request):
    user = request.user
    admin = False
    if user is not None and user.is_superuser:
        admin = True

    current_datetime = datetime.datetime.now()
    #current_time = datetime.datetime.now(timezone.timezone.utc).astimezone().tzinfo
    #user_timezone = timezone.localtime(timezone.now())
    text_calendar = calendar.TextCalendar().formatmonth(current_datetime.year, current_datetime.month).split('\n')
    width = len(text_calendar[1])
    text_calendar[0] += ' '*(width-len(text_calendar[0]))
    text_calendar[-2] += ' '*(width-len(text_calendar[-2]))
    text_calendar = '\n' + reduce(lambda x, y: x + '\n' + y, text_calendar)
    # print(text_calendar.replace(' ', '*'))
    tz = "UTC"
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

    response = requests.get("https://api.ipify.org/?format=json")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        ip_address = data["ip"]
        response = requests.get(f"https://ipinfo.io/{ip_address}/geo")
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            tz = data['timezone']

    partners = Partner.objects.all()
    context = {
        'admin': admin,
        'article': latest_article,
        'cat': cat_api,
        'dog': dog_api,
        'cur_time': current_datetime,
        'calendar': text_calendar,
        'tz': tz,
        'partners': partners
    }
    return render(request, 'HomePage.html', context)


def company_info_page(request):
    info = CompanyInfo.objects.order_by("date")
    return render(request, "CompanyInfoPage.html", {'info': reversed(info)})

def privacy_page(request):
    return render(request, "PrivacyAndPolicyPage.html")

def news_page(request):
    info = Article.objects.order_by("-date")
    return render(request, "NewsPage.html", {'news': info})


class ArticleDetailsView(DetailView):
    model = Article
    template_name = 'ArticleDetailsPage.html'
    context_object_name = 'article'


def employees_page(request):
    employees = Instructor.objects.all().order_by("fullname")
    paginator = Paginator(employees, 3)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "EmployeesPage.html", {'page_obj': page_obj})


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
    date = datetime.date.today()
    return render(request, "CouponsPage.html", {'coupons': coupons, 'date': date})


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


