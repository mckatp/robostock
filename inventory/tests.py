from django.test import TestCase
from django.urls import reverse
from .models import Category, Component

class ViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Sensors", description="Various sensors")
        self.component = Component.objects.create(
            name="Ultrasonic Sensor",
            category=self.category,
            quantity=10,
            location="Shelf A",
            description="HC-SR04"
        )

    def test_dashboard(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ultrasonic Sensor")

    def test_detail_view(self):
        response = self.client.get(reverse('component_detail', args=[self.component.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HC-SR04")
