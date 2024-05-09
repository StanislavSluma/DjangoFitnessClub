from django.test import TestCase
from django.urls import reverse
from .models import *
import requests


class HomePageViewTest(TestCase):
    def test_home_page_view_with_article(self):
        Article.objects.create(title='Test Article', text='This is a test article.', description='Description', date='2024-05-01')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'HomePage.html')

        self.assertIn('article', response.context)
        self.assertEqual(response.context['article'].title, 'Test Article')

    def test_home_page_view_no_articles(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.context.get('article'))

    def test_home_page_view_with_api_failure(self):
        from unittest.mock import patch

        with patch('requests.get') as mocked_get:
            mocked_get.return_value.status_code = 500
            response = self.client.get(reverse('home'))

            self.assertEqual(response.status_code, 200)
            self.assertIsNone(response.context.get('cat'))
            self.assertIsNone(response.context.get('dog'))


class CompanyInfoPageViewTest(TestCase):
    def test_company_info_page_view_with_data(self):
        pass


class NewsPageViewTest(TestCase):
    def test_news_page_view_with_articles(self):
        Article.objects.create(title='First News', text='Content 1', description='Desc 1', date='2024-05-01')
        Article.objects.create(title='Second News', text='Content 2', description='Desc 2', date='2024-05-02')

        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'NewsPage.html')

        self.assertEqual(len(response.context['news']), 2)

        self.assertEqual(response.context['news'][0].title, 'Second News')
        self.assertEqual(response.context['news'][1].title, 'First News')


class EmployeesPageViewTest(TestCase):
    def test_employees_page_view(self):
        response = self.client.get(reverse('employees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'EmployeesPage.html')


class FaqPageViewTest(TestCase):
    def test_faq_page_view(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FAQPage.html')


class VacanciesPageViewTest(TestCase):
    def test_vacancies_page_view(self):
        response = self.client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'VacanciesPage.html')

    def test_vacancies_page_view_no_vacancies(self):
        response = self.client.get(reverse('vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'VacanciesPage.html')

        self.assertEqual(len(response.context['vacancies']), 0)


class ReviewsPageViewTest(TestCase):
    def test_reviews_page_view(self):
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ReviewsPage.html')

    def test_reviews_page_view_no_reviews(self):
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ReviewsPage.html')

        self.assertEqual(len(response.context['reviews']), 0)


class CouponsPageViewTest(TestCase):
    def test_coupons_page_view(self):
        response = self.client.get(reverse('coupons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CouponsPage.html')

    def test_coupons_page_view_no_coupons(self):
        response = self.client.get(reverse('coupons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CouponsPage.html')

        self.assertEqual(len(response.context['coupons']), 0)


class InstructorsPageViewTest(TestCase):
    def test_instructors_page_view_with_parameters(self):
        # response = self.client.get(reverse('instructor', kwargs={'name': 'Alice', 'age': 35})) #how with kwargs i can send params?
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'InstructorsPage.html')
        #
        # self.assertEqual(response.context['name'], 'Alice')
        # self.assertEqual(response.context['age'], 35)
        #
        # self.assertIn('Alice', response.content.decode())
        # self.assertIn('35', response.content.decode())
        pass
