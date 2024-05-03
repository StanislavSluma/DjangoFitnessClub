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

from django.urls import path, re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from fitnes_club import views as fitness_view
from common_tasks import views as common_view


common_patterns = [
    path('', common_view.home_page, name='home'),
    path('info/', common_view.company_info_page, name='info'),
    path('news/', common_view.news_page, name='news'),
    path('faq/', common_view.faq_page, name='faq'),
    path('employees/', common_view.employees_page, name='employees'),
    path('vacancies/', common_view.vacancies_page, name='vacancies'),
    path('reviews/', common_view.reviews_page, name='feedback'),
    path('coupons/', common_view.coupons_page, name='coupons'),
]

account_patterns = [
    path('signin/', fitness_view.signin_page, name='signin'),
    path('login/', fitness_view.login_page, name='login'),
    path('logout/', fitness_view.logout_page, name='logout')
]


fitness_patterns = [
    path('', fitness_view.fitness_page, name='fitness'),
    path('user/', fitness_view.user_page, name='user'),
    path('client/', fitness_view.client_page, name='client'),
    path('instructor/', fitness_view.instructor_page, name='instructor')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fitness/', include(fitness_patterns)),
    path('home/', include(common_patterns)),
    path('account/', include(account_patterns))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
