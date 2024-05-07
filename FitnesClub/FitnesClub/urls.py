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


from common_tasks import views as common_view
from fitnes_club import views as fitness_view

common_patterns = [
    path('', common_view.home_page, name='home'),
    re_path(r'^info/$', common_view.company_info_page, name='info'),
    re_path(r'^news/$', common_view.news_page, name='news'),
    re_path(r'^faq/$', common_view.faq_page, name='faq'),
    re_path(r'^employees/$', common_view.employees_page, name='employees'),
    re_path(r'^vacancies/$', common_view.vacancies_page, name='vacancies'),
    re_path(r'^reviews/$', common_view.reviews_page, name='feedback'),
    re_path(r'^coupons/$', common_view.coupons_page, name='coupons'),
    re_path(r'^review/create/$', common_view.create_review_page, name='create_review')
]

account_patterns = [
    re_path(r'^signin/$', fitness_view.signin_page, name='signin'),
    re_path(r'^login/$', fitness_view.login_page, name='login'),
    re_path(r'^logout/$', fitness_view.logout_page, name='logout'),
]

instructor_patterns = [
    path('', fitness_view.instructor_page, name='instructor'),
    re_path(r'^change/$', fitness_view.instructor_change_page, name='instructor_change'),
    path('workout_clients<int:pk>/', fitness_view.workout_clients_page, name='workout_clients'),
]

client_patterns = [
    path('', fitness_view.client_page, name='client'),
    re_path(r'^change/$', fitness_view.client_change_page, name='client_change'),
    path('group<int:pk>/', fitness_view.client_group_page, name='group_details'),
    re_path(r'^groups/$', fitness_view.groups_page, name='groups'),
    path('groups/buy<int:pk>', fitness_view.group_buy_page, name='group_buy'),
    re_path(r'^club_card/$', fitness_view.client_club_card_page, name='client_buy_card')
]

super_user_patterns = [
    path('', fitness_view.super_user_page, name='super_user'),
    re_path(r'^age_chart/$', fitness_view.age_chart, name='age_chart'),
    re_path(r'^workout_chart/$', fitness_view.workout_chart, name='workout_chart')
]

fitness_patterns = [
    path('', fitness_view.fitness_page, name='fitness'),
    re_path(r'^user/$', fitness_view.user_page, name='user'),
    path('instructor<int:pk>/', fitness_view.InstructorDetailsView.as_view(), name='instructor_details'),
    re_path(r'^instructors/$', fitness_view.all_instructors_page, name='all_instructors'),
    re_path(r'^workouts/$', fitness_view.workouts_page, name='workouts'),
    re_path(r'^super_user/', include(super_user_patterns)),
    re_path(r'^client/', include(client_patterns)),
    re_path(r'^instructor/', include(instructor_patterns)),
]

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^fitness/', include(fitness_patterns)),
    re_path(r'^home/', include(common_patterns)),
    re_path(r'^account/', include(account_patterns))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
