from django.urls import path
from couriers.views import Transaction, DailyTransaction, WeeklyTransaction

app_name = 'couriers'

urlpatterns = [
	path('transaction/', Transaction.as_view(), name='transaction'),
	path('report/daily/<str:courier_name>/<str:date>/', DailyTransaction.as_view(), name='report-daily'),
	path('report/weekly/<str:courier_name>/<str:from_date>/<str:to_date>/', WeeklyTransaction.as_view(), name='report-weekly'),
]