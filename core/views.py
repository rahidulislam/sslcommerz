from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from core.models import BillingAddess, Order
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ

from core.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class PaymentViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_class = [IsAuthenticated]

    sslcz = SSLCOMMERZ(settings.SSL_COMMERZ)
    
    def create_payment(self, request):
        data=request.data
        print(request.user)
        data['user'] = request.user.pk
        print("data: ", data)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    def initial_payment(self, request,order_pk):
        order_instance = Order.objects.filter(pk=order_pk, user=request.user).exists()
        billing_user = BillingAddess.objects.filter(user=request.user).exists()
        if order_instance:
            order = Order.objects.get(pk=order_pk, user=request.user)
            bill_user = BillingAddess.objects.get(user=request.user)
            if order:
                payment_item = {
                    'total_amount': order.total_amount,
                    'currency': 'BDT',
                    'success_url': 'success url',
                    'fail_url': 'fail url',
                    'cancel_url': 'cancel_url',
                    'cus_name': order.cus_name,
                    'cus_email': order.cus_email,
                    'cus_phone': order.cus_phone,
                    'cus_add1': bill_user.address_line1,
                    'cus_city': bill_user.city,
                    'cus_country': bill_user.country,
                    'product_name': order.product_name,
                    'product_category': order.product_category,
                    'product_profile': 'general',
                    'num_of_item': order.num_of_item,
                    'tran_id': order.id,
                    'shipping_method': 'No'

                }
                response = self.sslcz.createSession(payment_item) # API response
                print(response)
                return Response(response, status.HTTP_200_OK)
            return Response({"message": "order not found"}, status.HTTP_404_NOT_FOUND)
        return Response(status.HTTP_400_BAD_REQUEST)