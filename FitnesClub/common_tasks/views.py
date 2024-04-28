from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Главная")


def instructors(request, name, age):
    return HttpResponse(f"""
                        <h2>О пользователе</h2>
                        <p> Имя: {name}</p>
                        <p> Возраст: {age}</p>
                        """)
