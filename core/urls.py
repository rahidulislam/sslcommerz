from django.urls import path
from core import views

app_name = 'core'

create_payment = views.PaymentViewset.as_view({
    "post": "create_payment"
})

initial_payment = views.PaymentViewset.as_view({
    "post": "initial_payment"
})

urlpatterns = [
    path('create/', create_payment, name='create-payment'),
    path('initial-payment/<int:order_pk>/', initial_payment, name='intial-payment')
]
