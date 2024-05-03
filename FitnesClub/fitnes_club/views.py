import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group as gr, User
from django.views.generic import DetailView

from .models import Client, Instructor, Workout
from common_tasks.models import CompanyInfo
from .forms import RegisterForm, LoginForm, FilterForm


def signin_page(request):
    if request.method == 'POST':
        fullname = request.POST['user_name']
        age = request.POST['age']
        phone_number = request.POST['phone_number']
        username = request.POST['login']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1 == password2:
            form = RegisterForm(request.POST)
            error = "Пароли должны совпадать"
            return render(request, 'SignInPage.html', {'form': form, 'error': error})
        if not re.fullmatch(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', phone_number):
            form = RegisterForm(request.POST)
            error = "Номер телефона должен соответствовать шаблону: +375 (ХХ) ХХХ-ХХ-ХХ"
            return render(request, 'SignInPage.html', {'form': form, 'error': error})
        user = User.objects.create_user(username=username, password=password1)
        user.groups.add(gr.objects.get(name='Client'))
        user.save()
        client = Client.objects.create(fullname=fullname, age=age, phone_number=phone_number, user=user)
        client.save()
        login(request, user)
        return HttpResponseRedirect('/fitness/client/')
    else:
        form = RegisterForm()
        return render(request, 'SignInPage.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Client').count():
                login(request, user)
                return HttpResponseRedirect('/fitness/client/')
            elif user.groups.filter(name='Instructor').count():
                login(request, user)
                return HttpResponseRedirect('/fitness/instructor/')
            else:
                return "ti kto?"
        else:
            form = LoginForm(request.POST)
            error = 'Пользователь не найден('
            return render(request, 'LogInPage.html', {'form': form, 'error': error})
    else:
        form = LoginForm()
        return render(request, 'LogInPage.html', {'form': form})


def client_check(user):
    return user.groups.filter(name='Client').count()


def instructor_check(user):
    return user.groups.filter(name='Instructor').count()


@login_required(login_url='/account/login')
def user_page(request):
    user = request.user
    if user.groups.filter(name='Client'):
        return HttpResponseRedirect('/fitness/client/')
    elif user.groups.filter(name='Instructor'):
        return HttpResponseRedirect('/fitness/instructor')
    else:
        return HttpResponseRedirect('/account/login')


@login_required(login_url='/account/login')
@user_passes_test(client_check, login_url="/account/login")
def client_page(request):
    user = request.user
    client = Client.objects.get(user=user)
    return render(request, "Client/ClientPage.html", {'client': client})


@login_required(login_url='/account/login')
@user_passes_test(instructor_check, login_url="/account/login")
def instructor_page(request):
    user = request.user
    instructor = Instructor.objects.get(user=user)
    return render(request, "Instructor/InstructorPage.html", {'instructor': instructor})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/fitness/')


def fitness_page(request):
    client_amount = Client.objects.all().count()
    info = CompanyInfo.objects.order_by('-date')[0]
    return render(request, 'FitnessPage.html', {'client_amount': client_amount, 'info': info})


def all_instructors_page(request):
    instructors = Instructor.objects.all()
    return render(request, "InstructorsPage.html", {'instructors': instructors})


class InstructorDetailsView(DetailView):
    model = Instructor
    template_name = 'InstructorDetailsPage.html'
    context_object_name = 'instructor'


def workouts_page(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            max_price = form.cleaned_data.get('max_price')
            if max_price == None:
                max_price = 2147483648
            workouts = Workout.objects.filter(price__lte=max_price, category__in=category)
            return render(request, "WorkoutsPage.html", {'form': form, 'workouts': workouts})
    else:
        form = FilterForm()
        workouts = Workout.objects.all()
    return render(request, "WorkoutsPage.html", {'form': form, 'workouts': workouts})
