import pytest
from django.http import Http404
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Client, Group, Hall, Workout, Instructor, GroupSchedule, ClubCard
from .forms import RegisterForm
from common_tasks.models import CompanyInfo
from .forms import ClientForm, InstructorForm
from datetime import datetime, timedelta


class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")

    def test_create_client(self):
        client = Client.objects.create(
            fullname="John Doe",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )
        self.assertEqual(client.fullname, "John Doe")

    def test_invalid_phone_number(self):
        client = Client(
            fullname="Invalid Phone",
            age=30,
            phone_number="123-45-67",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            client.clean()

    def test_negative_age(self):
        client = Client(
            fullname="Invalid Age",
            age=-1,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_empty_fullname(self):
        client = Client(
            fullname="",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_long_fullname(self):
        client = Client(
            fullname="x" * 101,
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_duplicate_user(self):
        with self.assertRaises(ValidationError):
            Client.objects.create(
                fullname="Jane Doe",
                age=30,
                phone_number="+375 (29) 123-45-67",
                user=self.user
            )


class GroupModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            fullname="John Doe",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=User.objects.create(username="anotheruser", password="password")
        )

    def test_create_group(self):
        group = Group.objects.create(name="Yoga Group", all_price=500)
        self.assertEqual(group.name, "Yoga Group")

    def test_group_with_clients(self):
        group = Group.objects.create(name="Yoga Group", all_price=500)
        group.clients.add(self.client)
        self.assertEqual(group.clients.count(), 1)

    def test_group_with_invalid_price(self):
        group = Group(name="Yoga Group", all_price=-100)
        with self.assertRaises(ValidationError):
            group.full_clean()

    def test_duplicate_group_name(self):
        Group.objects.create(name="Yoga Group", all_price=500)
        with self.assertRaises(ValidationError):
            Group.objects.create(name="Yoga Group", all_price=600)


class HallModelTest(TestCase):
    def test_create_hall(self):
        hall = Hall.objects.create(name="Main Hall", address="123 Street Name")
        self.assertEqual(hall.name, "Main Hall")

    def test_create_hall_with_empty_address(self):
        hall = Hall(name="Main Hall", address="")
        with self.assertRaises(ValidationError):
            hall.full_clean()

    def test_duplicate_hall_name(self):
        Hall.objects.create(name="Main Hall", address="123 Street Name")
        with self.assertRaises(ValidationError):
            Hall.objects.create(name="Main Hall", address="456 Another Street")


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Yoga Group", all_price=500)
        self.hall = Hall.objects.create(name="Main Hall", address="123 Street Name")

    def test_create_workout(self):
        workout = Workout.objects.create(
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            price=100,
            category="Yoga",
            group=self.group,
            hall=self.hall
        )
        self.assertEqual(workout.category, "Yoga")

    def test_workout_with_past_end_time(self):
        workout = Workout(
            start_time=datetime.now(),
            end_time=datetime.now() - timedelta(hours=1),
            price=100,
            category="Yoga",
            group=self.group,
            hall=self.hall
        )
        with self.assertRaises(ValidationError):
            workout.full_clean()

    def test_workout_without_group(self):
        workout = Workout(
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            price=100,
            category="Yoga",
            hall=self.hall
        )
        workout.full_clean()


class InstructorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testinstructor", password="testpassword")

    def test_create_instructor(self):
        instructor = Instructor.objects.create(
            fullname="Jane Doe",
            age=30,
            phone_number="+375 (29) 234-56-78",
            about="Fitness Instructor",
            user=self.user
        )
        self.assertEqual(instructor.fullname, "Jane Doe")

    def test_invalid_phone_number(self):
        instructor = Instructor(
            fullname="Invalid Phone",
            age=30,
            phone_number="123-45-67",
            about="Fitness Instructor",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            instructor.clean()

    def test_create_instructor_with_empty_about(self):
        instructor = Instructor(
            fullname="Jane Doe",
            age=30,
            phone_number="+375 (29) 234-56-78",
            user=self.user
        )
        instructor.full_clean()


class GroupScheduleModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Yoga Group", all_price=500)

    def test_create_group_schedule(self):
        group_schedule = GroupSchedule.objects.create(
            description="Yoga schedule",
            group=self.group
        )
        self.assertEqual(group_schedule.description, "Yoga schedule")

    def test_group_schedule_without_group(self):
        group_schedule = GroupSchedule(description="Yoga schedule")
        with self.assertRaises(ValidationError):
            group_schedule.full_clean()


class InstructorScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="instructor", password="testpassword")
        self.instructor = Instructor.objects.create(
            fullname="Jane Doe",
            age=30,
            phone_number="+375 (29) 234-56-78",
            about="Fitness Instructor",
            user=self.user
        )

    def test_create_instructor_schedule(self):
        instructor_schedule = InstructorSchedule.objects.create(
            description="Instructor Schedule",
            instructor=self.instructor
        )
        self.assertEqual(instructor_schedule.description, "Instructor Schedule")

    def test_instructor_schedule_without_instructor(self):
        instructor_schedule = InstructorSchedule(description="Instructor Schedule")
        with self.assertRaises(ValidationError):
            instructor_schedule.full_clean()


class ClubCardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testclient", password="testpassword")
        self.client = Client.objects.create(
            fullname="John Doe",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )

    def test_create_club_card(self):
        club_card = ClubCard.objects.create(
            name="Gold",
            end_date=datetime.now() + timedelta(days=365),
            discount=10,
            client=self.client
        )
        self.assertEqual(club_card.name, "Gold")

    def test_club_card_with_high_discount(self):
        club_card = ClubCard(
            name="Gold",
            end_date=datetime.now() + timedelta(days=365),
            discount=1000,
            client=self.client
        )


class ChangePagesViewsTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username="testuser", password="password123")

        self.instructor = Instructor.objects.create(
            user=self.test_user,
            fullname="Test Instructor",
            age=30,
            phone_number="123-456-7890",
        )

        self.client = Client.objects.create(
            user=self.test_user,
            fullname="Test Client",
            age=25,
            phone_number="098-765-4321",
        )

        self.auth_client = self.client
        self.client_logged_in = self.client.login(username=self.test_user.username, password="password123")

    def test_instructor_change_page_get(self):
        url = reverse("instructor_change")
        response = self.client_logged_in.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], InstructorForm)
        self.assertEqual(response.context["form"]["fullname"].value(), self.instructor.fullname)

    def test_instructor_change_page_post_valid(self):
        url = reverse("instructor_change")
        data = {
            "fullname": "Updated Instructor",
            "age": 35,
            "phone_number": "111-222-3333",
            "about": "Updated About",
            "login": "updateduser",
            "old_password": "",
        }
        response = self.client_logged_in.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/fitness/user/")

        self.instructor.refresh_from_db()
        self.assertEqual(self.instructor.fullname, "Updated Instructor")
        self.assertEqual(self.instructor.age, 35)
        self.assertEqual(self.instructor.phone_number, "111-222-3333")

    def test_instructor_change_page_post_invalid(self):
        url = reverse("instructor_change")
        data = {
            "fullname": "",
            "age": -1,
            "phone_number": "",
            "about": "",
            "login": "",
            "old_password": "",
        }
        response = self.client_logged_in.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.bulk_create([
            Client(fullname="Client A", age=30, phone_number="123456789"),
            Client(fullname="Client B", age=35, phone_number="987654321"),
        ])

        Instructor.objects.bulk_create([
            Instructor(fullname="Instructor A", age=40, phone_number="123456789"),
            Instructor(fullname="Instructor B", age=45, phone_number="987654321"),
        ])

        CompanyInfo.objects.bulk_create([
            CompanyInfo(history="Info A", date="2023-10-01"),
            CompanyInfo(history="Info B", date="2023-10-02"),
        ])

    def setUp(self):
        self.client = Client()

    def test_fitness_page(self):
        url = reverse("fitness")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("FitnessPage.html", response.template_name)
        self.assertIn("client_amount", response.context)
        self.assertEqual(response.context["client_amount"], 2)
        self.assertIn("info", response.context)
        self.assertEqual(response.context["info"].history, "Info B")

    def test_fitness_page_no_company_info(self):
        CompanyInfo.objects.all().delete()

        url = reverse("fitness")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("info", response.context)
        self.assertIsNone(response.context["info"])

    def test_all_instructors_page(self):
        url = reverse("all_instructors")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("InstructorsPage.html", response.template_name)
        self.assertIn("instructors", response.context)
        self.assertEqual(len(response.context["instructors"]), 2)

    def test_instructor_details_view(self):
        instructor = Instructor.objects.first()
        url = reverse("instructor_details", kwargs={"pk": instructor.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("InstructorDetailsPage.html", response.template_name)
        self.assertIn("instructor", response.context)
        self.assertEqual(response.context["instructor"].fullname, instructor.fullname)

    def test_instructor_details_view_not_found(self):
        url = reverse("instructor_details", kwargs={"pk": 999})
        with self.assertRaises(Http404):
            self.client.get(url)

    def test_all_instructors_page_empty(self):
        Instructor.objects.all().delete()

        url = reverse("all_instructors")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("instructors", response.context)
        self.assertEqual(len(response.context["instructors"]), 0)


@pytest.fixture
def test_client():
    return Client()


@pytest.fixture
def setup_groups():
    group, _ = Group.objects.get_or_create(name='Client')
    return group


@pytest.mark.django_db
def test_signin_page_get(test_client):
    url = reverse("signin_page")
    response = test_client.get(url)

    assert response.status_code == 200
    assert "SignInPage.html" in response.template_name
    assert "form" in response.context
    assert isinstance(response.context["form"], RegisterForm)


@pytest.mark.django_db
def test_signin_page_post_valid(test_client, setup_groups):
    url = reverse("signin_page")
    data = {
        "user_name": "John Doe",
        "age": 25,
        "phone_number": "+375 (44) 123-45-67",
        "login": "johndoe",
        "password1": "securepassword",
        "password2": "securepassword",
    }
    response = test_client.post(url, data)

    assert response.status_code == 302
    assert response.url == "/fitness/client/"

    user = User.objects.get(username="johndoe")
    assert user is not None
    assert user.check_password("securepassword")

    client = Client.objects.get(user=user)
    assert client.fullname == "John Doe"
    assert client.age == 25
    assert client.phone_number == "+375 (44) 123-45-67"

    client_group = Group.objects.get(name="Client")
    assert client_group in user.groups.all()


@pytest.mark.django_db
def test_signin_page_post_password_mismatch(test_client, setup_groups):
    url = reverse("signin_page")
    data = {
        "user_name": "Jane Doe",
        "age": 30,
        "phone_number": "+375 (44) 123-45-67",
        "login": "janedoe",
        "password1": "password1",
        "password2": "password2",
    }
    response = test_client.post(url, data)

    assert response.status_code == 200
    assert "form" in response.context
    assert isinstance(response.context["form"], RegisterForm)
    assert "Пароли должны совпадать" in response.context.get("error", "")


@pytest.mark.django_db
def test_signin_page_post_invalid_phone(test_client, setup_groups):
    url = reverse("signin_page")
    data = {
        "user_name": "Invalid Phone",
        "age": 25,
        "phone_number": "123456789",
        "login": "invalidphone",
        "password1": "securepassword",
        "password2": "securepassword",
    }
    response = test_client.post(url, data)

    assert response.status_code == 200
    assert "form" in response.context
    assert isinstance(response.context["form"], RegisterForm)
    assert "Номер телефона должен соответствовать шаблону" in response.context.get("error", "")

