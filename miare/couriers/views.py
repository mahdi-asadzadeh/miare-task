import datetime

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from couriers import models
from couriers import use_case
from couriers import serializers


class Transaction(generics.GenericAPIView):
    serializer_class = serializers.CreateTransaction

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            amount = serializer.data.get('amount')
            date = serializer.data.get('date')
            courier_name = serializer.data.get('courier_name')

            format_date = "%Y-%m-%d %H:%M:%S"
            date = datetime.datetime.strptime(date, format_date)

            use_case.CouriersIncome.create_tx(
                amount=amount, 
                date=date,
                courier_name=courier_name,
            )
            return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeeklyTransaction(generics.GenericAPIView):
    serializer_class = serializers.Transaction

    def get(self, request, courier_name, from_date, to_date):
        try:
            result = use_case.CouriersIncome.get_weekly_income(
                from_date=from_date,
                to_date=to_date,
                courier_name=courier_name,
            )
            return Response({"income": result, "message": "Successful"}, status=status.HTTP_200_OK)

        except models.Courier.DoesNotExist:
            return Response({"income": None, "message": "Courier does not exist!"}, status=status.HTTP_404_NOT_FOUND)


class DailyTransaction(generics.GenericAPIView):
    serializer_class = serializers.DailyTransaction

    def get(self, request, courier_name, date):
        try:
            tx_daily = use_case.CouriersIncome.get_daily_income(
                date=date, 
                courier_name=courier_name,
            )
            result = self.serializer_class(tx_daily).data
            return Response({"income": result, "message": "Successful"}, status=status.HTTP_200_OK)

        except models.TransactionDaily.DoesNotExist:
            return Response({"income": None, "message": "Transaction daily does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        except models.Courier.DoesNotExist:
            return Response({"income": None, "message": "Courier does not exist!"}, status=status.HTTP_404_NOT_FOUND)
