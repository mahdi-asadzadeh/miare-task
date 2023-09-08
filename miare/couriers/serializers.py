from rest_framework.serializers import ModelSerializer, CharField, DateTimeField

from couriers import models


class Transaction(ModelSerializer):

	class Meta:
		model = models.Transaction
		fields = ['amount', 'date']


class CreateTransaction(ModelSerializer):
	courier_name = CharField()
	date = DateTimeField("%Y-%m-%d %H:%M:%S")

	class Meta:
		model = models.Transaction
		fields = ['amount', 'date', 'courier_name']


class DailyTransaction(ModelSerializer):
	transactions = Transaction(many=True, read_only=True)

	class Meta:
		model = models.TransactionDaily
		fields = ['date', 'amount', 'transactions']
