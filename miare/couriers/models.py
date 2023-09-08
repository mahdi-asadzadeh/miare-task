from django.db import models


class Courier(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'


class TransactionDaily(models.Model):
    date = models.DateField()
    amount = models.IntegerField(default=0)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name="daily_transactions")
    
    def __str__(self):
        return f'Transaction daily on {self.date} amount: {self.amount} name: {self.courier.name}'


class Transaction(models.Model):
    # CHOICES_TYPE = (
    #     ('ADEDUCTION_FROM_INCOME', 'Deduction from income'),
    #     ('INCREASE_INCOME', 'Increase income'),
    #     ('INCOME', 'Income'),
    # )
    # type = models.CharField(max_length=23, choices=CHOICES_TYPE)
    
    date = models.DateTimeField()
    amount = models.IntegerField()
    tx_daily = models.ForeignKey(TransactionDaily, on_delete=models.CASCADE, related_name="transactions")

    def __str__(self):
        return f'Transaction on {self.date} amount: {self.amount} name: {self.tx_daily.courier.name}'
