import datetime

from django.test import TestCase

from couriers import models
from couriers.use_case import CouriersIncome


class TransactionDaily(TestCase):

    def test_get_daily_income_success(self):
        format_date = "%Y-%m-%d %H:%M:%S"

        models.Courier.objects.create(
            name="test2"
        )

        new_tx_1 = CouriersIncome.create_tx(
            amount=25, 
            date=datetime.datetime.strptime("2023-09-09 15:25:00", format_date),
            courier_name="test2"
        )
        new_tx_2 = CouriersIncome.create_tx(
            amount=25, 
            date=datetime.datetime.strptime("2023-09-09 15:26:00", format_date),
            courier_name="test2"
        )

        tx_daily = CouriersIncome.get_daily_income(
            date="2023-09-09", 
            courier_name="test2",
        )

        self.assertEqual(tx_daily.amount, 50)
        self.assertEqual(tx_daily.courier.name, "test2")

    def test_does_not_exist_tx_daily(self):
        models.Courier.objects.create(
            name="test1"
        )

        try:
            CouriersIncome.get_daily_income(date="2023-09-09", courier_name="test1")
        except Exception as e:
            self.assertIsInstance(e, models.TransactionDaily.DoesNotExist)
