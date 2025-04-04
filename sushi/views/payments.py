import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Order, Payment


class PaymentIntentAPIView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)

            # Generate unique transaction ID
            transaction_id = f"PAY-{uuid.uuid4().hex[:10].upper()}"

            # Create pending payment
            payment = Payment.objects.create(
                order=order,
                method_id=request.data.get("method_id"),
                amount=order.total_price,
                transaction_id=transaction_id,
            )

            return Response(
                {
                    "transaction_id": transaction_id,
                    "amount": order.total_price,
                    "payment_url": f"/api/payments/confirm/{transaction_id}/",
                }
            )

        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PaymentConfirmationAPIView(APIView):
    def post(self, request, transaction_id):
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)

            # Simulate payment processing
            if request.data.get("confirm", False):
                payment.status = "COMPLETED"
                payment.order.status = "PREPARING"

                payment.order.save()
                payment.save()
                return Response({"status": "Payment completed"})

            payment.status = "FAILED"
            payment.save()
            return Response(
                {"status": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Payment.DoesNotExist:
            return Response(
                {"error": "Invalid transaction ID"}, status=status.HTTP_404_NOT_FOUND
            )
