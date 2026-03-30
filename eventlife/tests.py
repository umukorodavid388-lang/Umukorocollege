from django.test import TestCase, Client
from django.utils import timezone
from .models import Event, EventCategory
import datetime


class CalendarAPITest(TestCase):
	def setUp(self):
		self.client = Client()
		cat = EventCategory.objects.create(text='Test')
		# create event on 15th of current month
		now = timezone.localtime(timezone.now())
		self.year = now.year
		self.month = now.month
		self.day = 15
		dt = datetime.datetime(self.year, self.month, self.day, 10, 0)
		Event.objects.create(
			title='Test Event',
			description='Desc',
			image='media/events/test.jpg',
			date=dt,
			eventcategories=cat,
			start_time=datetime.time(10,0),
			end_time=datetime.time(12,0),
			location='Here'
		)

	def test_calendar_api_returns_event(self):
		resp = self.client.get(f'/events/api/calendar/?year={self.year}&month={self.month}')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertTrue(data.get('success'))
		days = data.get('days', {})
		self.assertIn(str(self.day), days)
