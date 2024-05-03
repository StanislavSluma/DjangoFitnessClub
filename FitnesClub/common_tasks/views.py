import requests
from django.shortcuts import render
from .models import Article, CompanyInfo, Coupon, Faq, Vacancy, Employee, Review


def home_page(request):
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
    return render(request, 'HomePage.html', {'article': latest_article, 'cat': cat_api, 'dog': dog_api})


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
