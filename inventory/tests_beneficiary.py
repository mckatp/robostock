from django.test import TestCase
from django.urls import reverse
from .models import Category, Component, Beneficiary, Transaction
from django.contrib.auth.models import User

class BeneficiaryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='staff', password='password', is_staff=True)
        self.client.login(username='staff', password='password')
        self.category = Category.objects.create(name="Sensors")
        self.component = Component.objects.create(name="Sensor A", category=self.category, quantity=10)
        self.beneficiary = Beneficiary.objects.create(name="John Doe", role="Student", added_by=self.user)

    def test_beneficiary_list(self):
        response = self.client.get(reverse('beneficiary_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_checkout_to_beneficiary(self):
        response = self.client.post(reverse('checkout_component', args=[self.component.pk]), {
            'borrower': self.beneficiary.pk,
            'quantity_taken': 2
        })
        self.assertEqual(response.status_code, 302)
        self.component.refresh_from_db()
        self.assertEqual(self.component.quantity, 8)
        self.assertTrue(Transaction.objects.filter(borrower=self.beneficiary).exists())
