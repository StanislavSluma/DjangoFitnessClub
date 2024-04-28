"""
URL configuration for FitnesClub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from fitnes_club import views as fitness_view
from common_tasks import views as common_view
from django.urls import path, include
from django.contrib import admin


common_patterns = [
    path('about/', common_view.index),
    path('instructors/', common_view.instructors, {'name': 'Mama', 'age': 18})
]


fitness_patterns = [
    path('clients/', fitness_view.clients),
    path('client/<int:id>', fitness_view.client)
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fitness/', include(fitness_patterns)),
    path('', include(common_patterns))
]
