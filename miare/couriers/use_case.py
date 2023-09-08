import datetime

from django.db.models import F
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import TruncWeek

from couriers import models


class CouriersIncome:

    @staticmethod
    def create_tx(
        amount: int, 
        date: datetime.datetime,
        courier_name: str,
    ) -> models.Transaction:

        courier = models.Courier.objects.get(name=courier_name)
        tx_daily, _ = models.TransactionDaily.objects.get_or_create(
            date=date.date(), 
            courier=courier,
        )

        # the F() object to generate an SQL expression that describes the required operation at the database level.
        tx_daily.amount = F('amount') + amount
        tx_daily.save()

        tx = models.Transaction.objects.create(
            date=date,
            amount=amount,
            tx_daily=tx_daily,
        )
        return tx

    @staticmethod
    def get_daily_income(
        date: str,
        courier_name: str,
    ) -> models.TransactionDaily:
        courier = models.Courier.objects.get(name=courier_name)
        tx_daily = models.TransactionDaily.objects.get(
            date=date, 
            courier=courier,
        )
        return tx_daily

    @staticmethod
    def get_weekly_income(
        from_date: str,
        to_date: str,
        courier_name: str,
    ) -> dict:
        courier = models.Courier.objects.get(name=courier_name)

        weekly_transactions = models.TransactionDaily.objects.\
            filter(date__gte=from_date, date__lte=to_date, courier=courier).\
            annotate(
                week=TruncWeek('date')
            ).\
            values('week').\
            annotate(
                total_count=Count('id'),
                total_amount=Sum('amount')
            ).\
            order_by('week')
        
        result = []
        for entry in weekly_transactions:
            week_start = entry['week']
            week_end = week_start + datetime.timedelta(days=6)  # Assuming a week is 7 days
            total_count = entry['total_count']
            total_amount = entry['total_amount']

            # Get the transactions for the current week
            week_transactions = models.TransactionDaily.objects.filter(
                date__gte=week_start, 
                date__lte=week_end,
            )

            week_tx = {
                "week": {
                    "week_start": week_start,
                    "week_end": week_end
                },
                "total_amount": total_amount,
                "transaction_count": total_count,
                "transactions": [{"amount": tx.amount, "date": tx.date, "week_day": tx.date.strftime('%A')} for tx in week_transactions]
            }
            result.append(week_tx)

        return result
