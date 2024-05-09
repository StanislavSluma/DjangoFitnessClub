import calendar
import datetime
import os
import random
import re
import io
import matplotlib
from django.db.models.fields import related

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import logging

from FitnesClub.settings import BASE_DIR
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import Group as gr, User
from django.views.generic import DetailView
from django.db.models import Avg, Count, Sum, Max
from datetime import timedelta

from .models import Client, Instructor, Workout, Group, ClubCard
from common_tasks.models import CompanyInfo, Coupon
from .forms import RegisterForm, LoginForm, FilterForm, InstructorForm, ClientForm


logger = logging.getLogger(__name__)
logger2 = logging.getLogger('fitnes_club_war')


def signin_page(request):
    logger.info("INFO: User in signin page ")
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
            logger2.warning("WAR: User password mismatch ")
            return render(request, 'SignInPage.html', {'form': form, 'error': error})
        if not re.fullmatch(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', phone_number):
            form = RegisterForm(request.POST)
            error = "Номер телефона должен соответствовать шаблону: +375 (ХХ) ХХХ-ХХ-ХХ"
            logger2.warning("WAR: User phone_number does not match with pattern ")
            return render(request, 'SignInPage.html', {'form': form, 'error': error})
        user = User.objects.create_user(username=username, password=password1)
        user.groups.add(gr.objects.get(name='Client'))
        user.save()
        client = Client.objects.create(fullname=fullname, age=age, phone_number=phone_number, user=user)
        client.save()
        login(request, user)
        logger.info("INFO: User signin successful ")
        # return HttpResponseRedirect('/fitness/client/')
        return HttpResponseRedirect(reverse('client'))
    else:
        form = RegisterForm()
        return render(request, 'SignInPage.html', {'form': form})


def login_page(request):
    logger.info("INFO: User in login page ")
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Client').count():
                login(request, user)
                logger.info("INFO: User is Client")
                # return HttpResponseRedirect('/fitness/client/')
                return HttpResponseRedirect(reverse('client'))
            elif user.groups.filter(name='Instructor').count():
                login(request, user)
                logger.info("INFO: User is Instructor")
                # return HttpResponseRedirect('/fitness/instructor/')
                return HttpResponseRedirect(reverse('instructor'))
            elif user.is_superuser:
                login(request, user)
                logger.info("INFO: User is superuser ")
                return HttpResponseRedirect(reverse('super_user'))
            else:
                form = LoginForm(request.POST)
                error = 'Пользователь не найден('
                logger2.warning("WAR: User not found")
                return render(request, 'LogInPage.html', {'form': form, 'error': error})
        else:
            form = LoginForm(request.POST)
            error = 'Пользователь не найден('
            logger2.warning("WAR: User not authorized")
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
        # return HttpResponseRedirect('/fitness/client/')
        return HttpResponseRedirect(reverse('client'))
    elif user.groups.filter(name='Instructor'):
        # return HttpResponseRedirect('/fitness/instructor/'))
        return HttpResponseRedirect(reverse('instructor'))
    elif user.is_superuser:
        # return HttpResponseRedirect('/fitness/super_user/'))
        return HttpResponseRedirect(reverse('super_user'))
    else:
        # return HttpResponseRedirect('/account/login/')
        return HttpResponseRedirect(reverse('login'))


@login_required(login_url='/account/login')
@user_passes_test(client_check, login_url="/account/login")
def client_page(request):
    user = request.user
    client = Client.objects.get(user=user)
    groups = client.group_set.all()
    return render(request, "Client/ClientPage.html", {'client': client, 'groups': groups})


@login_required(login_url='/account/login')
@user_passes_test(client_check, login_url="/account/login")
def client_club_card_page(request):
    user = request.user
    client = Client.objects.get(user=user)
    client.expenses += 20
    end_date = datetime.datetime.today() + datetime.timedelta(days=365)
    discount = random.randint(1, 20)
    if discount <= 5:
        name = 'Обычная клубная карта'
    elif discount <= 10:
        name = 'Удачливая клубная карта'
    elif discount <= 15:
        name = 'Очень удачливая клубная карта'
    else:
        name = 'Невероятно удачливая клубная карта'
    try:
        client.clubcard = ClubCard.objects.update(name=name, discount=discount, end_date=end_date, client=client)
    except:
        client.clubcard.delete()
        client.clubcard = ClubCard.objects.create(name=name, discount=discount, end_date=end_date, client=client)
    client.save()
    return HttpResponseRedirect(reverse('user'))


@login_required(login_url='/account/login')
@user_passes_test(client_check, login_url="/account/login")
def client_group_page(request, id):
    group = Group.objects.get(id=id)
    workouts = group.workout_set.all()
    return render(request, "Client/GroupDetailsPage.html", {'group': group, 'workouts': workouts})


@login_required(login_url='/account/login')
@user_passes_test(client_check, login_url="/account/login")
def groups_page(request):
    client = Client.objects.get(user=request.user)
    groups = Group.objects.filter(is_open=True).exclude(id__in=client.group_set.all())
    return render(request, "Client/GroupsPage.html", {'groups': groups})


@login_required(login_url='/account/login')
@user_passes_test(client_check, login_url="/account/login")
def group_buy_page(request, id):
    group = Group.objects.get(id=id)
    if request.method == "POST":
        client = Client.objects.get(user=request.user)
        client.group_set.add(group)
        coupon = Coupon.objects.filter(code=request.POST['coupon'])
        if coupon.count() and coupon[0].end_date > datetime.date.today():
            coupon = coupon[0].discount
        else:
            coupon = 0
        if client.clubcard.end_date > datetime.date.today():
            coupon += client.clubcard.discount
        client.expenses += group.all_price * (100 - coupon) / 100
        if group.max_clients <= group.clients.count():
            group.is_open = False
        client.save()
        return HttpResponseRedirect(reverse('client'))
    workouts = group.workout_set.all()
    return render(request, "Client/GroupBuyPage.html", {'group': group, 'workouts': workouts})


@login_required(login_url='/account/login')
@user_passes_test(instructor_check, login_url="/account/login")
def instructor_page(request):
    user = request.user
    instructor = Instructor.objects.get(user=user)
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    today = datetime.datetime.today()
    tomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    today = datetime.datetime(today.year, today.month, today.day)
    workouts = instructor.workouts.filter(start_time__lte=tomorrow).filter(start_time__gte=today).order_by('start_time')

    return render(request, "Instructor/InstructorPage.html", {'instructor': instructor, 'schedule': workouts})


@login_required(login_url='/account/login')
@user_passes_test(instructor_check, login_url="/account/login")
def workout_clients_page(request, id):
    workout = Workout.objects.get(id=id)
    clients = workout.group.clients.all()
    return render(request, "Instructor/WorkoutClientsPage.html", {'clients': clients})


def logout_page(request):
    logout(request)
    # return HttpResponseRedirect('/fitness/')
    return HttpResponseRedirect(reverse('fitness'))


def fitness_page(request):
    logger.info("mama")
    logger2.warning("papa")
    print(request.session.get('timezone_offset'))
    # print(datetime.datetime.now())
    # print(datetime.datetime.utcnow())
    c = calendar.TextCalendar()
    d = datetime.date.today()
    s = c.formatmonth(d.year, d.month)
    print(s)
    print(c)
    client_amount = Client.objects.all().count()
    info = CompanyInfo.objects.order_by('-date')
    if info:
        info = info[0]
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


@login_required(login_url='/account/login')
@user_passes_test(instructor_check, login_url="/account/login")
def instructor_change_page(request):
    if request.method == "POST":
        form = InstructorForm(request.POST)
        if not form.is_valid():
            return render(request, "Instructor/ChangePage.html", {'form': form})
        instructor = Instructor.objects.get(user=request.user)
        instructor.fullname = request.POST['fullname']
        instructor.age = request.POST['age']
        instructor.phone_number = request.POST['phone_number']
        instructor.about = request.POST['about']
        if request.FILES:
            if os.path.exists(str(BASE_DIR) + instructor.photo.url):
                os.remove(str(BASE_DIR) + instructor.photo.url)
            instructor.photo = request.FILES['photo']
        if request.POST['old_password']:
            error = None
            if not instructor.user.check_password(request.POST['old_password']):
                error = "Введенный пароль не совпадает с действительным"
            if request.POST['password1'] != request.POST['password2']:
                error = "Пароли должны совпадать"
            if not request.POST['password1']:
                error = "Поле пароля не должно быть пустым"
            if not request.POST['login']:
                error = "Поле логина не должно быть пустым"
            if error:
                form = InstructorForm(request.POST)
                return render(request, "Instructor/ChangePage.html", {'form': form, 'error': error})
            instructor.user.set_password(request.POST['password1'])
            instructor.user.username = request.POST['login']
            instructor.user.save()
        instructor.save()
        # return HttpResponseRedirect('/fitness/user/')
        return HttpResponseRedirect(reverse('user'))
    else:
        instructor = Instructor.objects.get(user=request.user)
        form = InstructorForm({'fullname': instructor.fullname,
                               'age': instructor.age,
                               'phone_number': instructor.phone_number,
                               'about': instructor.about,
                               'photo': instructor.photo,
                               'login': instructor.user.username
                               })
    return render(request, "Instructor/ChangePage.html", {'form': form})


@login_required(login_url='/account/login')
@user_passes_test(client_check, login_url="/account/login")
def client_change_page(request):
    client = Client.objects.get(user=request.user)

    if request.method == "POST":
        form = ClientForm(request.POST)
        if not form.is_valid():
            return render(request, "Client/ChangePage.html", {'form': form})

        if request.POST['old_password']:
            if client.user.check_password(request.POST['old_password']):
                client.user.set_password(request.POST['password1'])
                client.user.username = request.POST['login']
                client.user.save()
            else:
                error = "Введенный пароль не совпадает с действительным"
                return render(request, "Client/ChangePage.html", {'form': form, 'error': error})

        client.fullname = form.cleaned_data.get('fullname')
        client.age = form.cleaned_data.get('age')
        client.phone_number = form.cleaned_data.get('phone_number')
        client.save()
        # return HttpResponseRedirect('/fitness/user/')
        return HttpResponseRedirect(reverse('user'))

    form = ClientForm({'fullname': client.fullname,
                       'age': client.age,
                       'phone_number': client.phone_number,
                       'login': client.user.username})
    return render(request, "Client/ChangePage.html", {'form': form})


@login_required(login_url='admin/')
@user_passes_test(lambda user: user.is_superuser, login_url='admin/')
def super_user_page(request):

    #statistics
    clients = Client.objects.all().order_by("fullname")

    total_expenses = clients.aggregate(Sum("expenses"))

    avg_expenses = clients.aggregate(Avg("expenses"))

    avg_age = clients.aggregate(Avg("age"))["age__avg"]

    now = datetime.datetime.now()
    one_month_ago = now - timedelta(days=30)
    group_workouts = Group.objects.annotate(
        total_workouts=Count("workout", filter=models.Q(workout__start_time__gte=one_month_ago, workout__start_time__lte=now))
    )

    client_services = clients.annotate(
        total_services=Sum("group__workout__price")
    )

    workout_categories = Workout.objects.values("category").annotate(
        count=Count("id")
    ).order_by("-count")

    profitable_workouts = Workout.objects.values("category").annotate(
        total_revenue=Sum("price")
    ).order_by("-total_revenue")


    context = {
        "clients": clients,
        "total_expenses": total_expenses["expenses__sum"],
        "avg_expenses": avg_expenses["expenses__avg"],
        "avg_age": avg_age,
        "group_workouts": group_workouts,
        "client_services": client_services,
        "workout_categories": workout_categories,
        "profitable_workouts": profitable_workouts,
    }
    return render(request, 'SuperUserPage.html', context)


def age_chart(request):
    age_distribution = (
        Client.objects.values("age").annotate(count=Count("id")).order_by("age")
    )
    age_labels = [item["age"] for item in age_distribution]
    age_counts = [item["count"] for item in age_distribution]
    plt.figure(figsize=(10, 6))
    plt.bar(age_labels, age_counts, color='skyblue')
    plt.xlabel("Возраст")
    plt.ylabel("Клиент")
    plt.title("Распределение возраста клиентов")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')


def workout_chart(request):
    now = datetime.datetime.now()
    one_month_ago = now - timedelta(days=30)
    group_workouts = Group.objects.annotate(
        total_workouts=Count("workout", filter=models.Q(workout__start_time__gte=one_month_ago))
    )
    group_names = [group.name for group in group_workouts]
    workout_counts = [group.total_workouts for group in group_workouts]

    plt.figure(figsize=(10, 6))
    plt.bar(group_names, workout_counts, color='b')
    plt.xlabel("Группы")
    plt.ylabel("Итоговое количество занятий(30 дней)")
    plt.title("Распределение занятий про группам за 30 дней")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')
