from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.orders import Order
from ..serializers.orders import OrderSerializer
from ..utils.permissions import IsOwnerOrReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ["COMPLETED", "CANCELLED"]:
            order.status = "CANCELLED"
            order.save()
            return Response({"status": "order cancelled"})
        return Response(
            {"error": "Order cannot be cancelled"}, status=status.HTTP_400_BAD_REQUEST
        )
