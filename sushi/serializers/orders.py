from rest_framework import serializers

from ..models.orders import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["sushi", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "total_price",
            "delivery_address",
            "items",
            "created_at",
        ]
        read_only_fields = ["user", "total_price", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        total_price = 0

        for item_data in items_data:
            sushi = item_data["sushi"]
            quantity = item_data["quantity"]
            price = sushi.price * quantity
            total_price += price

            OrderItem.objects.create(
                order=order, sushi=sushi, quantity=quantity, price=price
            )

        order.total_price = total_price
        order.save()
        return order
