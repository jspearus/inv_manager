from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Component


class ComponentPageTests(TestCase):
    def test_inventory_page_shows_empty_state(self):
        response = self.client.get(reverse("inventory:component_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your inventory is empty")

    def test_inventory_search_matches_partial_text_in_component_fields(self):
        resistor = Component.objects.create(
            name="Resistor",
            value="10kΩ",
            description="Carbon film through-hole",
            quantity=25,
            location="Drawer A3",
        )
        Component.objects.create(
            name="Blue LED",
            value="5mm",
            description="Through-hole indicator",
            quantity=8,
            location="Bin 2",
        )

        response = self.client.get(reverse("inventory:component_list"), {"q": "10k"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, resistor.name)
        self.assertNotContains(response, "Blue LED")
        self.assertContains(response, 'value="10k"')

        response = self.client.get(reverse("inventory:component_list"), {"q": "sist"})

        self.assertContains(response, resistor.name)

        response = self.client.get(reverse("inventory:component_list"), {"q": "carbon"})

        self.assertContains(response, resistor.name)

        response = self.client.get(reverse("inventory:component_list"), {"q": "drawer"})

        self.assertContains(response, resistor.name)

    def test_inventory_search_shows_no_results_message(self):
        Component.objects.create(name="10k resistor", quantity=25, location="Drawer A3")

        response = self.client.get(reverse("inventory:component_list"), {"q": "transistor"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No components found")

    def test_component_can_be_added_from_form(self):
        response = self.client.post(
            reverse("inventory:component_create"),
            {
                "name": "Resistor",
                "value": "10kΩ",
                "description": "Carbon film",
                "quantity": 25,
                "location": "Drawer A3",
            },
        )

        self.assertRedirects(response, reverse("inventory:component_list"))
        component = Component.objects.get()
        self.assertEqual(
            (
                component.name,
                component.value,
                component.description,
            ),
            ("Resistor", "10kΩ", "Carbon film"),
        )

    def test_negative_quantity_is_rejected(self):
        response = self.client.post(
            reverse("inventory:component_create"),
            {
                "name": "Resistor",
                "value": "10kΩ",
                "quantity": -1,
                "location": "Drawer A3",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Component.objects.exists())

    def test_component_can_be_updated_and_deleted(self):
        component = Component.objects.create(name="LED", quantity=8, location="Bin 2")
        response = self.client.post(
            reverse("inventory:component_update", args=[component.pk]),
            {
                "name": "LED",
                "value": "Red",
                "description": "High brightness",
                "quantity": 6,
                "location": "Bin 4",
            },
        )

        self.assertRedirects(response, reverse("inventory:component_list"))
        component.refresh_from_db()
        self.assertEqual(
            (
                component.name,
                component.value,
                component.description,
                component.quantity,
                component.location,
            ),
            ("LED", "Red", "High brightness", 6, "Bin 4"),
        )

        response = self.client.post(reverse("inventory:component_delete", args=[component.pk]))

        self.assertRedirects(response, reverse("inventory:component_list"))
        self.assertFalse(Component.objects.exists())


class ComponentApiTests(APITestCase):
    def test_api_lists_components(self):
        Component.objects.create(name="LED", quantity=8, location="Bin 2")

        response = self.client.get("/api/components/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "LED")
        self.assertEqual(response.data[0]["quantity"], 8)

    def test_api_searches_partial_text_in_component_fields(self):
        Component.objects.create(
            name="Resistor",
            value="10kΩ",
            description="Carbon film through-hole",
            quantity=25,
            location="Drawer A3",
        )
        Component.objects.create(
            name="Blue LED",
            value="5mm",
            description="Through-hole indicator",
            quantity=8,
            location="Bin 2",
        )

        for query in ("sist", "10k", "carbon", "drawer"):
            with self.subTest(query=query):
                response = self.client.get("/api/components/", {"search": query})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]["name"], "Resistor")

    def test_api_creates_component(self):
        response = self.client.post(
            "/api/components/",
            {
                "name": "Capacitor",
                "value": "100µF",
                "description": "Electrolytic",
                "quantity": 12,
                "location": "Drawer B1",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        component = Component.objects.get()
        self.assertEqual(
            (component.value, component.description, component.location),
            ("100µF", "Electrolytic", "Drawer B1"),
        )

    def test_api_rejects_negative_quantity(self):
        response = self.client.post(
            "/api/components/",
            {"name": "Capacitor", "quantity": -1, "location": "Drawer B1"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Component.objects.exists())

    def test_api_updates_and_deletes_component(self):
        component = Component.objects.create(name="LED", quantity=8, location="Bin 2")

        response = self.client.patch(
            f"/api/components/{component.pk}/",
            {"quantity": 5},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        component.refresh_from_db()
        self.assertEqual(component.quantity, 5)

        response = self.client.delete(f"/api/components/{component.pk}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Component.objects.exists())
