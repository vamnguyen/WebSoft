from django.urls import path
from ..views.payment import CreatePaymentAPIView,GetAllPaymentDetailAPIView ,GetPaymentDetailAPIView

urlpatterns = [
    path('payment/create/', CreatePaymentAPIView.as_view(), name='create_payment'),
    path('payment/', GetAllPaymentDetailAPIView.as_view(), name='get_all_payment_detail'),
    path('payment/<int:pk>/', GetPaymentDetailAPIView.as_view(), name='get_payment_detail')
]